import xml.dom.minidom
import xmltodict
from ncclient import manager
import ncclient

try:
    m = manager.connect(
        host="192.168.60.3",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )
except ncclient.transport.errors.SSHError:
    print("Unable to connect to router netconfig is not activated")


netconf_filter = """
<filter>
 <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
"""

netconf_eth = """
<filter>
 <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
"""
netconf_route = """
<filter>
 <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"/>
</filter>
"""

netconf_run = m.get_config(source="running")
netconf_reply = m.get(filter=netconf_filter)
netconf_port = m.get(filter=netconf_eth)
netconf_route = m.get(filter=netconf_route)

netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
netconf_reply_port = xmltodict.parse(netconf_port.xml)
netconf_reply_static = xmltodict.parse(netconf_route.xml)


for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
    print("Name: {} MAC: {}".format(
                interface["name"],
                interface["phys-address"]))

for interface in netconf_reply_port["rpc-reply"]["data"]["interfaces"]["interface"]:
    print("\nName: {}".format(interface["name"]))
    print("Description: {}".format(interface["description"]))
    if len(interface["ipv4"]) > 1:
        print("IPV4: {}".format(interface["ipv4"]["address"]["ip"]))
        print("Netmask: {}".format(interface["ipv4"]["address"]["netmask"]))
    if len(interface["ipv6"]) > 1:
        print("IPV6: {}".format(interface["ipv6"]["address"]["ip"]))
        print("Netmask: {}".format(interface["ipv6"]["address"]["netmask"]))

for interface in netconf_reply_static["rpc-reply"]["data"]["routing"]["routing-instance"]["routing-protocols"]["routing-protocol"]["static-routes"]["ipv4"]["route"]:
    print("\n-------------------------")
    print("      Static routes \n")

    print("Destination: {}".format(interface["destination-prefix"]))
    print("Destination: {}".format(interface["next-hop"]["outgoing-interface"]))
