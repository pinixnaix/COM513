"""
python dictionary called network
network consists of 1 switch and 2 routers

"""

switch=["S1"]
router=["R1", "R2"]
network={"S1":"10.0.1.1", "R1":["10.0.2.1", "10.0.3.1", "10.0.4.1"], "R2":["10.0.5.1", "10.0.6.1", "10.0.7.1"]}

print(f"{switch[0]}")
print(type(network))
