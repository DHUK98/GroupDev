import json
import os

stat = []
with open('static/stations.json') as json_file:
    data = json.load(json_file)
    stat = data

print(stat)

# for s in stat:
#     path = "data/stations/" + s["ID"]
#
#     try:
#         os.mkdir(path)
#     except OSError:
#         print("error")

for s in stat:
    with open('data/stations/'+s["ID"]+"/info.json", 'w') as f:
        json.dump(s, f)
