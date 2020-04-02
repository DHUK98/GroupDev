'''
Module for converting data to/from json
'''

from netCDF4 import Dataset
import ujson as json
import os


def json_from_netcdf_file(filepath, with_keys=False):
    f = Dataset(filepath, "r", format="NETCDF4")

    datas = {}
    keys = []
    for v in f.variables.keys():
        new_v = v
        if v == "latitude":
            new_v = "lat"
        if v == "longitude":
            new_v = "lon"
        keys.append(new_v)
        datas[new_v] = (f.variables[v][:].tolist())
    f.close()

    data_json = json.dumps(datas, sort_keys=True)

    if with_keys:
        return data_json, json.dumps(keys)
    return data_json



if __name__ == "__main__":
    path = '../static/stations/CGR/'
    files = []
    for file in os.listdir(path):
        if file.endswith(".nc"):
            files.append(file)

    for f in files:
        test, keys = json_from_netcdf_file("../static/stations/CGR/" + f, with_keys=True)
        json_f = f.replace(".nc", ".json")
        with open("../static/stations/CGR/" + json_f, 'w') as outfile:
            outfile.write(test)
        with open("../static/stations/CGR/keys_" + json_f, 'w') as outfile:
            outfile.write(keys)
