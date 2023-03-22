"""
Program in python to fetch network measurement data from RIPE ATLAS using the API provided.
"""
from ripe.atlas.cousteau import AtlasLatestRequest
from ripe.atlas.cousteau import Measurement
from ripe.atlas.sagan import PingResult
from ripe.atlas.sagan import TracerouteResult
import json
import requests
import urllib3
from ncclient import manager, xml_
import ncclient

urllib3.disable_warnings()
basicauth = ("cisco", "cisco123!")
headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }


def get_measurements():
    """"Function that accepts a measurement ID value from the user """
    msm_id = input("Insert a measurement ID: ")
    measurement = Measurement(id=msm_id)
    print("Measurement type: ", measurement.type)
    if measurement.type != 'ping' and measurement.type != 'traceroute':
        print("Please insert a valid ID measurement for a ping or traceroute\n")
        get_measurements()

    return msm_id, measurement.type


def get_ping_results(msm_id):
    """"Function that requests the Ping results """
    kwargs = {"msm_id": msm_id}
    success, results = AtlasLatestRequest(**kwargs).create()
    average = PingResult(results[0])
    if not success:
        print("\nMeasurement ID not valid!\n")
        run()
    else:
        return average.rtt_average, average.destination_address


def get_traceroute_results(msm_id):
    """"Function that requests the traceroute results """
    kwargs = {"msm_id": msm_id}
    success, results = AtlasLatestRequest(**kwargs).create()
    average = TracerouteResult(results[0])
    msm_rtt = []
    for hop in average.hops:
        item = hop.median_rtt
        if item is not None:
            msm_rtt.append(item)

    return msm_rtt, average.destination_address


def check_router_restconf():
    api_url = "https://192.168.60.3/restconf"
    check = requests.get(api_url, auth=basicauth, verify=False)
    if check.status_code == 200:
        return True
    return False


def check_router_netconf():
    try:
        manager.connect(
            host="192.168.60.3",
            port=830,
            username="cisco",
            password="cisco123!",
            hostkey_verify=False
        )
    except ncclient.transport.errors.SSHError:
        return False
    return True


def menu():
    print("=" * 75)
    print("Please choose one of the options to perform the configuration on the router")
    choices = [1, 2]
    print("[1] RESTCONF")
    print("[2] NETCONF")
    option = int(input("Option: "))
    if option in choices:
        return option
    else:
        print("Wrong Option!!!!!")
        menu()


def get_customer_id(cust):
    print()
    print("=" * 75)
    print(f"\t\t\t\t\t\t     Costumer {cust}\n")
    results = []
    ip = []

    for item in range(3):
        msm_id, msm_type = get_measurements()
        if msm_type == 'ping':
            rtt, origin = get_ping_results(msm_id)
            if rtt is not None:
                results.append(rtt)
                ip.append(origin)
        elif msm_type == 'traceroute':
            rtt, origin = get_traceroute_results(msm_id)
            if rtt is not None:
                results.append(rtt)
                ip.append(origin)
    return [results.index(min(results))+1, ip[results.index(min(results))]]


def add_loopback_netconfig(isp):
    m = manager.connect(
        host="192.168.60.3",
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
    api_url = "https://192.168.60.3/restconf/data/ietf-interfaces:interfaces"
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

    if 200 <= resp.status_code <= 299:
        print(f"Loopback{cust} with a Link to ISP{cust} added successfully!!")
    else:
        print(f"Error adding Loopback{cust}")


def add_static_netconfig(isp, ip):
    print("=" * 75)
    print("Auto Configuration of a static route")
    m = manager.connect(
        host="192.168.60.3",
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
    print("=" * 75)
    print("Auto Configuration of a static route")
    api_url = "https://192.168.60.3/restconf/data/ietf-routing:routing"
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

    if 200 <= resp.status_code <= 299:
        print(f"Configuration of a static route to {ip} via Loopback{isp}")
    else:
        print("Error in the configuration of a static route")


def save_config_netconf():
    m = manager.connect(
        host="192.168.60.3",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )

    save = """
    <cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>
    """
    m.dispatch(xml_.to_ele(save))
    m.close_session()


def save_config_restconf():
    api_url = "https://192.168.60.3/restconf/operations/cisco-ia:save-config"
    resp = requests.post(api_url, auth=basicauth, headers=headers, verify=False)
    if 200 <= resp.status_code <= 299:
        print(f"Running Config saved successful into Startup Config")
    else:
        print("Error in Running Config saved successful into Startup Config")


def run():
    """Main Function"""
    print("=" * 75)
    print("\t\t\t\t     Router Automation challenge!\n")
    if check_router_netconf() is True:
        print("NETCONF is enabled!")
    else:
        print("NETCONF is disabled!")
    if check_router_restconf() is True:
        print("RESTCONF is enabled!\n")
    else:
        print("RESTCONF is disabled!\n")

    option = menu()
    print()
    print("=" * 75)
    print("Auto Loopback configuration")
    if option == 1:
        for loop in range(3):
            add_loopback_restconfig(loop+1)
        for customer in range(3):
            isp, ip = get_customer_id(customer+1)
            add_static_restconfig(isp, ip)
        save_config_restconf()
    elif option == 2:
        for loop in range(3):
            add_loopback_netconfig(loop+1)
        for customer in range(3):
            isp, ip = get_customer_id(customer+1)
            add_static_netconfig(isp, ip)
        save_config_netconf()


if __name__ == "__main__":
    run()
