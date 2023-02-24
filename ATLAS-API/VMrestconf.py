import json
import requests
import urllib3

urllib3.disable_warnings()


api_url = "https://192.168.60.3/restconf/data/ietf-interfaces:interfaces"
#api_url = "https://192.168.60.3/restconf/data/ietf-routing:routing"



headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }

basicauth = ("cisco", "cisco123!")


resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

response_json = resp.json()

print(json.dumps(response_json, indent=4))
