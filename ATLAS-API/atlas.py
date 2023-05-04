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
    kwargs = {"msm_id": msmid}
    msm_result = {}
    sucess, results = AtlasLatestRequest(**kwargs).create()
    msm_result = results[0]

    if not sucess:
        print("\nMeasurement ID not valid!\n")
        run()
    else:
        check_type(msmid, results)
        return msm_result


def check_type(msmid, results):
    """"Function that detects the measurement ID type of the RIPE atlas database """
    measurement = Measurement(id=msmid)
    print("\nMeasurement type: ", measurement.type)
    if measurement.type == 'ping' or measurement.type == 'traceroute':
        with open("RIPEmeasurements.txt", "a", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
    else:
        print("Please!! Only ping or traceroute measurements!!")
        run()


def display_results(msmid, results):
    """"Function that displays the results from the RIPE atlas database """
    measurement = Measurement(id=msmid)
    if measurement.type == 'ping':
        data = PingResult(results)
        print("\nAddress Family: IPV", data.af)
        print("Source Address: ", data.origin)
        print("Destination Address: ", data.destination_address)
        print("Packets sent: ", data.packets_sent)
        print("Median Round Trip: ", data.rtt_median)
        print("Average Round Trip: ", data.rtt_average)

    elif measurement.type == 'traceroute':
        data = TracerouteResult(results)
        print("\nAddress Family: ", data.af)
        print("Source Address: ", data.origin)
        print("Destination Address: ", data.destination_address)
        print("Total hops: ", data.total_hops)
        mrtt = []
        for hop in data.hops:
            if hop.median_rtt is not None:
                mrtt.append(hop.median_rtt)
        new_mrtt = sorted(mrtt)
        mid = len(new_mrtt) // 2
        res = (new_mrtt[mid] + new_mrtt[-mid-1]) / 2
        print(f"Median Round Trip: {res:.3f}")


def run():
    """Main Function"""
    msmid = get_id()
    results = get_results(msmid)
    display_results(msmid, results)


if __name__ == "__main__":
    run()
