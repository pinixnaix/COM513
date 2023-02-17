"""
Program in python to fetch network measurement data from RIPE ATLAS using the API provided.
"""
import json
from ripe.atlas.cousteau import AtlasLatestRequest
from ripe.atlas.cousteau import Measurement
from ripe.atlas.sagan import PingResult
from ripe.atlas.sagan import TracerouteResult


def get_measurements():
    """"Function that accepts a measurement ID value from the user """
    msm_id = input("\nInsert a measurement id: ")
    measurement = Measurement(id=msm_id)
    print("Measurement type: ", measurement.type)
    return msm_id, measurement.type


def get_ping_results(msm_id):
    """"Function that requests the Ping results """
    kwargs = {"msm_id": msm_id}
    success, results = AtlasLatestRequest(**kwargs).create()

    average = PingResult(results[0])

    if not success:
        print("\nMeasurement ID not valid!\n")
        run()
    else:
        return average.rtt_average


def get_traceroute_results(msm_id):
    """"Function that requests the traceroute results """
    kwargs = {"msm_id": msm_id}
    success, results = AtlasLatestRequest(**kwargs).create()

    average = TracerouteResult(results[0])

    msm_rtt = []
    for hop in average.hops:
        msm_rtt.append(hop.median_rtt)

    return msm_rtt


def run():
    """Main Function"""
    results = []
    msm_id, msm_type = get_measurements()
    if msm_type == 'ping':
        results.append(get_ping_results(msm_id))
        while True and len(results) < 3:
            msm_id, msm_type = get_measurements()
            if msm_type == 'ping':
                results.append(get_ping_results(msm_id))
    elif msm_type == 'traceroute':
        results = get_traceroute_results(msm_id)
    #display_results(msmid, results)
    print(results)
    print(min(results))
    print(results.index(min(results)))


if __name__ == "__main__":
    run()
