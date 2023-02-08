from ripe.atlas.cousteau import AtlasLatestRequest
from ripe.atlas.cousteau import measurement

kwargs = {"msm_id":int(input("Insert a measurement id: "))}

sucess, results = AtlasLatestRequest(**kwargs).create()

if sucess:
    print(results)
