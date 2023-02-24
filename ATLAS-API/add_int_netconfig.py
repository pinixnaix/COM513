from ncclient import manager
import xml.dom.minidom

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
    <name>2</name>
    <description>Loopback to ISP2</description>
    <ip>
     <address>
      <primary>
       <address>200.200.200.2</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_data)

print("Success? {}".format(netconf_reply.ok))

print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
