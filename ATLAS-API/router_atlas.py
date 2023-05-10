"""
Program in python to fetch network measurement data from RIPE ATLAS using the API provided.
Select the measurement using its ID value
Compare 3 measurements
Create a configuration for the router
Apply configuration to the router
"""
from ripe.atlas.cousteau import AtlasLatestRequest
from ripe.atlas.cousteau import Measurement
from ripe.atlas.sagan import PingResult
from ripe.atlas.sagan import TracerouteResult
import json
import requests
import urllib3
from ncclient import manager, xml_

urllib3.disable_warnings()

basicauth = ("cisco", "cisco123!")
headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }
# Router IP address, change the ip if router has different ip address
router_ip_add = "192.168.60.3"


def get_measurements():
    """"
    Function that accepts a measurement ID value from the user
    Requests the results of the measurement ID value from RIPE atlas database
    Confirms the validity of the given measurement ID value
    Detects the type of the measurement ID value
    Returns the type and results of the measurement ID value given
    """
    # While loop the run until the 2 IF statements are True
    while True:
        msm_id = input("Insert a measurement ID: ")
        kwargs = {"msm_id": msm_id}
        measurement = Measurement(id=msm_id)
        # Requesting the results from the RIPE atlas database
        success, results = AtlasLatestRequest(**kwargs).create()
        # If statement to verify the validity of the given measurement ID value
        if success:
            # If statement to detect the measurement ID type
            if check_type(measurement):
                # command to stop the while loop when the previous 2 if statements are true
                break
        else:
            print("---Measurement ID not valid!---")

    return measurement.type, results


def check_type(measurement):
    """"
    Function that detects the measurement ID type of the RIPE atlas database
    Returns True or False depending of the measurement type
    """
    print("\nMeasurement type: ", measurement.type)
    # If statement to verify the measurement ID type is a ping or a traceroute
    # and returns True
    if measurement.type == 'ping' or measurement.type == 'traceroute':
        return True
    else:
        # else is other type prints an error message and returns False
        print("---Please!! Only ping or traceroute measurements!!---")
        return False


def get_ping_results(results):
    """"
    Function that analyses the Ping results
    Returns the average Round Trip Time and the destination
    IP address from the ping results
    """
    average = PingResult(results[0])
    return average.rtt_average, average.destination_address


def get_traceroute_results(results):
    """"
    Function that analyses the traceroute results
    Calculates the Median round trip time of all the hops from the traceroute
    Returns the Median Round Trip Time and the destination
    IP address from the traceroute results
    """
    average = TracerouteResult(results[0])
    msm_rtt = []
    # For loop to iterate through all hops from the traceroute
    for hop in average.hops:
        # If statement to verify hop median round trip time is not null
        if hop.median_rtt is not None:
            # appends all valid hop median round trip time values into a list
            msm_rtt.append(hop.median_rtt)
    # calculates the median round trip of all the hops median round trips
    new_mrtt = sorted(msm_rtt)
    mid = len(new_mrtt) // 2
    res = (new_mrtt[mid] + new_mrtt[-mid - 1]) / 2

    return res, average.destination_address


def menu():
    """
    Function that prints a menu on the console and gives the user the
    opportunity to choose between RESTCONF or NETCONF to configure the router
    Returns the chosen option
    """
    print("=" * 75)
    print("Please choose one of the options to perform the configuration on the router")
    choices = [1, 2]
    print("[1] RESTCONF")
    print("[2] NETCONF")
    # while loop to run until a correct option is chosen
    while True:
        option = int(input("Option: "))
        # if statement to confirm if the given option is one of the available
        if option in choices:
            # command to stop the while loop when the previous if statement is true
            break
        print("---Wrong Option! Please choose a correct option!---")
    return option


def get_customer_id(cust):
    """
    Function that will get 3 measurements ID values from the user for the Customer
    Compare the 3 values
    Returns the lowest of the 3 values and respective destination IP address
    """
    print()
    print("=" * 75)
    print(f"\t\t\t\t\t\t     Costumer {cust}\n")
    average = []
    ip = []

    # for loop to get 3 measurements ID values from the user for the customer
    for item in range(3):
        msm_type, results = get_measurements()
        # if statement to verify if the measurement type is a ping
        if msm_type == 'ping':
            # retrieve from the ping results the average round trip time and destination ip address
            rtt, origin = get_ping_results(results)
            # If statement to verify average round trip time is not null
            if rtt is not None:
                # appends valid average round trip time value and destination ip address into a list
                average.append(rtt)
                ip.append(origin)
        # if statement to verify if the measurement type is a traceroute
        elif msm_type == 'traceroute':
            # retrieve from the traceroute results the median
            # round trip time and destination ip address
            rtt, origin = get_traceroute_results(results)
            # If statement to verify median round trip time is not null
            if rtt is not None:
                # appends valid median round trip time value and destination ip address into a list
                average.append(rtt)
                ip.append(origin)
    # returns the index (1,2,3) from the round trip time list that belongs to the lowest value in the list
    # and its correspondent ip address from the ip addresses list
    return [average.index(min(average))+1, ip[average.index(min(average))]]


def add_loopback_netconfig(isp):
    """Function to add a loopback interface to the router using NETCONF """
    m = manager.connect(
        host=router_ip_add,
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )

    netconf_data = """
    <config>
     <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <interface>
       <Loopback>
        <name>"""+str(isp)+"""</name>
        <description>Link to ISP"""+str(isp)+"""</description>
        <ip>
         <address>
          <primary>
           <address>"""+str(isp)+"""0.0.0.1</address>
           <mask>255.0.0.0</mask>
          </primary>
         </address>
        </ip>
       </Loopback>
      </interface>
     </native>
    </config>
    """
    netconf_reply = m.edit_config(target="running", config=netconf_data)

    if netconf_reply.ok is True:
        print(f"Loopback{isp} with a Link to ISP{isp} added successfully!!")
    else:
        print(f"Error adding Loopback{isp}")
    m.close_session()


def add_loopback_restconfig(cust):
    """Function to add a loopback interface to the router using RESTCONF """

    api_url = "https://"+router_ip_add+"/restconf/data/ietf-interfaces:interfaces"
    yang_config = {
        "ietf-interfaces:interface": {
            "name": "Loopback"+str(cust),
            "description": "Loopback to ISP"+str(cust),
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": str(cust)+"0.0.0.1",
                        "netmask": "255.0.0.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.post(api_url, data=json.dumps(yang_config), auth=basicauth, headers=headers, verify=False)
    # If statement to verify the request made was successful
    if 200 <= resp.status_code <= 299:
        print(f"Loopback{cust} with a Link to ISP{cust} added successfully!!")
    else:
        print(f"Error adding Loopback{cust}")


def add_static_netconfig(isp, ip):
    """Function to add a static route to the router using NETCONF """

    print("=" * 75)
    print("Auto Configuration of a static route")
    m = manager.connect(
        host=router_ip_add,
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )

    netconf_data = """
    <config>
       <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
          <routing-instance>
             <name>default</name>
             <description>default-vrf [read-only]</description>
             <interfaces/>
             <routing-protocols>
                <routing-protocol>
                   <type>static</type>
                   <name>1</name>
                   <static-routes>
                      <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing">

                         <route>
                            <destination-prefix>"""+str(ip)+"""/32</destination-prefix>
                            <next-hop>
                               <outgoing-interface>Loopback"""+str(isp)+"""</outgoing-interface>
                            </next-hop>
                         </route>
                      </ipv4>
                   </static-routes>
                </routing-protocol>
             </routing-protocols>
          </routing-instance>
       </routing>
    </config>
    """

    netconf_reply = m.edit_config(target="running", config=netconf_data)

    if netconf_reply.ok is True:
        print(f"Configuration of a static route to {ip} via Loopback{isp}")
    else:
        print("Error in the configuration of a static route")
    m.close_session()


def add_static_restconfig(isp, ip):
    """Function to add a static route to the router using RESTCONF """

    print("=" * 75)
    print("Auto Configuration of a static route")
    api_url = "https://"+router_ip_add+"/restconf/data/ietf-routing:routing"
    yang_config = {
        "ietf-routing:routing": {
            "routing-instance": [
                {
                    "name": "default",
                    "description": "default-vrf [read-only]",
                    "routing-protocols": {
                        "routing-protocol": [
                            {
                                "type": "ietf-routing:static",
                                "name": "1",
                                "static-routes": {
                                    "ietf-ipv4-unicast-routing:ipv4": {
                                        "route": [
                                            {
                                                "destination-prefix": str(ip)+"/32",
                                                "next-hop": {
                                                    "outgoing-interface": "Loopback"+str(isp)
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }

    resp = requests.patch(api_url, data=json.dumps(yang_config), auth=basicauth, headers=headers, verify=False)
    # If statement to verify the request made was successful
    if 200 <= resp.status_code <= 299:
        print(f"Configuration of a static route to {ip} via Loopback{isp}")
    else:
        print("Error in the configuration of a static route")


def save_config_netconf():
    """Function to save the running configuration into the startup configuration to the router using NETCONF """
    print("\n"+"=" * 75)
    m = manager.connect(
        host=router_ip_add,
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )
    save = """<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>"""
    reply = m.dispatch(xml_.to_ele(save))
    if reply.ok is True:
        print(f"Running Config saved successful into Startup Config")
    else:
        print("Error in Running Config saved successful into Startup Config")
    print("=" * 75)
    m.close_session()


def save_config_restconf():
    """Function to save the running configuration into the startup configuration to the router using RESTCONF """
    print("\n"+"=" * 75)
    api_url = "https://"+router_ip_add+"/restconf/operations/cisco-ia:save-config"
    resp = requests.post(api_url, auth=basicauth, headers=headers, verify=False)
    # If statement to verify the request made was successful
    if 200 <= resp.status_code <= 299:
        print(f"Running Config saved successful into Startup Config")
    else:
        print("Error in Running Config saved successful into Startup Config")
    print("=" * 75)


def run():
    """Main Function"""
    print("=" * 75)
    print("\t\t\t\t     Router Automation challenge!")
    # calls the function to print a menu in the console for the user to chose between NETCONF or RESTCONF
    option = menu()
    print("=" * 75)
    print("\t\t\t\t     Auto Loopback configuration\n")
    # If statement to verify if the chosen option is 1 - to use RESTCONF
    if option == 1:
        # for loop to add 3 loopback interfaces using RESTCONF
        for loop in range(3):
            add_loopback_restconfig(loop+1)
        # for loop to add a static route for the 3 customers using RESTCONF
        for customer in range(3):
            isp, ip = get_customer_id(customer+1)
            add_static_restconfig(isp, ip)
        # call the function to save the configuration on the router using RESTCONF
        save_config_restconf()

    # If statement to verify if the chosen option is 2 - to use NETCONF
    elif option == 2:
        # for loop to add 3 loopback interfaces using NETCONF
        for loop in range(3):
            add_loopback_netconfig(loop+1)
        # for loop to add a static route for the 3 customers using NETCONF
        for customer in range(3):
            isp, ip = get_customer_id(customer+1)
            add_static_netconfig(isp, ip)
        # call the function to save the configuration on the router using NETCONF
        save_config_netconf()


if __name__ == "__main__":
    run()
