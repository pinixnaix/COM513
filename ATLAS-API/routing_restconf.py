import json
import requests
import urllib3

urllib3.disable_warnings()


api_url = "https://192.168.60.3/restconf/data/ietf-routing:routing"

headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }

basicauth = ("cisco", "cisco123!")

yangConfig = {
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
                                            "destination-prefix": "30.30.30.3/32",
                                            "next-hop": {
                                                "outgoing-interface": "Loopback2"
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

resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)


if 200 <= resp.status_code <= 299:
    print("STATUS OK: {}".format(resp.status_code))
else:
    print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
