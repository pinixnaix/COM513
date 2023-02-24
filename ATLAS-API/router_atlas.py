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
import xml.dom.minidom
import xmltodict
from ncclient import manager
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
        return average.rtt_average


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
    return msm_rtt


def check_router_restconf():
    api_url = "https://192.168.60.3/restconf"
    check = requests.get(api_url, auth=basicauth, verify=False)
    if check.status_code == 200:
        return True
    return False


def check_router_netconf():
    try:
        m = manager.connect(
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
    msm_id, msm_type = get_measurements()
    while len(results) < 2:
        if msm_type == 'ping':
            results.append(get_ping_results(msm_id))
        elif msm_type == 'traceroute':
            results = get_traceroute_results(msm_id)
        msm_id, msm_type = get_measurements()

    return [results.index(min(results))+1, msm_id]

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

def add_loopback_restconfig():
    return
def add_static_netconfig():
   return
def add_static_restconfig():
    return

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
    print()
    print("=" * 75)
    print("Auto Loopback configuration")
    for customer in range(3):
        add_loopback_netconfig(customer+1)

    #isp, msm_id = get_customer_id(customer)
    #option = menu()


if __name__ == "__main__":
    run()
