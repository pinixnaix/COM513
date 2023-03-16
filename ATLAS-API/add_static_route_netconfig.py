from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="192.168.60.3",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)
"""
netconf_data =
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
                        <destination-prefix>20.20.20.2/32</destination-prefix>
                        <next-hop>
                           <outgoing-interface>Loopback2</outgoing-interface>
                           <next-hop-address>
                        </next-hop>
                     </route>
                  </ipv4>
               </static-routes>
            </routing-protocol>
         </routing-protocols>
      </routing-instance>
   </routing>
</config>


netconf_reply = m.edit_config(target="running", config=netconf_data)

print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
"""
data = """
<?xml version="1.0" encoding="utf-8"?>
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="">
  <cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>
</rpc>
"""
netconf_reply = m.edit_config(target="running", config=data)

print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
