import json
import requests
import urllib3

urllib3.disable_warnings()


api_url = "https://192.168.60.3/restconf/operations/cisco-ia:save-config"

headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }

basicauth = ("cisco", "cisco123!")

resp = requests.post(api_url, auth=basicauth, headers=headers, verify=False)

print(resp)


#POST https://<IP:Port>/netconf/operations/cisco-ia:save-config