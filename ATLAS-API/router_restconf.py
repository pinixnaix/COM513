import json
import requests
import urllib3

urllib3.disable_warnings()


api_url = "https://192.168.60.3/restconf/data/ietf-interfaces:interfaces"

headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }

basicauth = ("cisco", "cisco123!")

yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback3",
        "description": "Loopback to ISP3",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.10.10.10",
                    "netmask": "255.255.255.252"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

resp = requests.post(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

if 200 <= resp.status_code <= 299:
    print("STATUS OK: {}".format(resp.status_code))
else:
    print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
