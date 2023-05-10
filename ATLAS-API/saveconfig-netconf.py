from ncclient import manager, xml_

print("\n"+"=" * 75)
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
reply = m.dispatch(xml_.to_ele(save))
if reply.ok is True:
    print(reply)

print("=" * 75)
m.close_session()
