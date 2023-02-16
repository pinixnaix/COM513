"""
Program in python to fetch network measurement data from RIPE ATLAS using the API provided.
Select the measurement using its ID value
Display the measurement data in the console
"""
import json
from ripe.atlas.cousteau import AtlasLatestRequest
from ripe.atlas.cousteau import Measurement
from ripe.atlas.sagan import PingResult
from ripe.atlas.sagan import TracerouteResult


def get_id():
    """"Function that accepts a measurement ID value from the user """
    msmid = input("Insert a measurement id: ")
    return msmid

def get_results(msmid):
    """"Function that requests the results from the RIPE atlas database """
    kwargs = {"msm_id":msmid}
    sucess, results = AtlasLatestRequest(**kwargs).create()
    if sucess:
        with open ("RIPEmeasurements.txt", "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        return results
    else:
        print("\nMeasurement ID not valid!\n")
        run()


def display_results(msmid, results):
    """"Function that displays the results from the RIPE atlas database """
    measurement = Measurement(id= msmid)
    print("\nMeasurement type: ",measurement.type)
    if measurement.type == 'ping':
        for result in results:
            data = PingResult(result)
            print("\nAddress Family: IPV",data.af)
            print("Source Address: ",data.origin)
            print("Destination Address: ",data.destination_address)
            print("Packets sent: ",data.packets_sent)
            print("Median Round Trip: ",data.rtt_median)
            print("Average Round Trip: ",data.rtt_average)
        
        
        

    elif measurement.type == 'traceroute':
        for result in results:
            data = TracerouteResult(result)
            print("\nAddress Family: ",data.af)
            print("Source Address: ",data.origin)
            print("Destination Address: ",data.destination_address)
            print("Total hops: ",data.total_hops)
            print("Median Round Trip: ",data.hops)
        

def run():

    msmid = get_id()
    results = get_results(msmid)
    display_results(msmid, results)
        
if __name__ == "__main__":
    run()