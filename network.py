"""
python dictionary called network
network consists of 1 switch and 2 routers

"""

network={"S1":["10.0.1.1"],
"R1":["10.0.2.1", "10.0.3.1", "10.0.4.1"],
"R2":["10.0.5.1", "10.0.6.1", "10.0.7.1"]}

print(type(network))

for key, values in network.items():
    print(key, end=" ")
    for ip in values:
        print(ip, end=" ")
    print()
