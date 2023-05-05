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
    sucess, results = AtlasLatestRequest(**kwargs).create()
    msm_result = results[0]
    # If statement to verify the measurement ID given is valid
    if not sucess:
        # If the measurement is not valid, calls the main function
        print("\nMeasurement ID not valid!\n")
        run()
    else:
        # If is valid calls the function check_type to detect the measurement ID type
        check_type(msmid, results)
        return msm_result


def check_type(msmid, results):
    """"Function that detects the measurement ID type of the RIPE atlas database """
    measurement = Measurement(id=msmid)
    print("\nMeasurement type: ", measurement.type)
    # If statement to verify the measurement ID type is a ping or a traceroute
    if measurement.type == 'ping' or measurement.type == 'traceroute':
        # if true it stores the results in a file using fragmented JSON format
        # appends new queries to the file
        with open("RIPEmeasurements.txt", "a", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
    else:
        # if is other type prints a error message and calls the main function
        print("Please!! Only ping or traceroute measurements!!")
        run()


def display_results(msmid, results):
    """"Function that displays the results from the RIPE atlas database """
    measurement = Measurement(id=msmid)
    # If statement to verify the measurement ID type is a ping
    if measurement.type == 'ping':
        # Display: Address family, Source and Destination IP addresses,
        #         number of packet sent, average round trip time of the measurement
        data = PingResult(results)
        print("\nAddress Family: IPV", data.af)
        print("Source Address: ", data.origin)
        print("Destination Address: ", data.destination_address)
        print("Packets sent: ", data.packets_sent)
        print("Median Round Trip: ", data.rtt_median)
        print("Average Round Trip: ", data.rtt_average)

    # If statement to verify the measurement ID type is a traceroute
    elif measurement.type == 'traceroute':
        # Display: Address Family, Source address, Destination address,
        #          Total Hops, and Median Round trip time.
        data = TracerouteResult(results)
        print("\nAddress Family: ", data.af)
        print("Source Address: ", data.origin)
        print("Destination Address: ", data.destination_address)
        print("Total hops: ", data.total_hops)
        mrtt = []
        # For loop to iterate through all hops from the traceroute
        for hop in data.hops:
            # If statement to verify hop median round trip is not null
            if hop.median_rtt is not None:
                # appends all valid hop median round trip values into a list
                mrtt.append(hop.median_rtt)
        # calculates the median round trip of all the hops median round trips
        new_mrtt = sorted(mrtt)
        mid = len(new_mrtt) // 2
        res = (new_mrtt[mid] + new_mrtt[-mid-1]) / 2

        print(f"Median Round Trip: {res:.3f}")


def run():
    """Main Function"""
    # calls the function get_id and stores the return value into a variable
    msmid = get_id()
    # calls the function get_results with the measurement id
    # and stores the return value into a variable
    results = get_results(msmid)
    # calls the function display_results with the measurement id and results
    display_results(msmid, results)


if __name__ == "__main__":
    run()
