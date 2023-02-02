"""
Application to process all the data
"""

import urllib.parse
import requests
import json

def url(main,key,loc,dest):
    """ function to get the url from the data"""
    url = main + urllib.parse.urlencode({"key": key, "from":loc, "to":dest})
    return url

def retrieve_json(link):
    """  function to retrieve the jason data from the url given"""
    jason_data = requests.get(link).json()
    with open("path.json", "w") as file:
        json.dump(jason_data, file, indent=4)

    return jason_data
