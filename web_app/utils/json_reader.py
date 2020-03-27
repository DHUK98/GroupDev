'''
Module for converting data to/from json
'''

from netCDF4 import Dataset
import ujson as json
import os


def json_from_netcdf_file(filepath):
    f = Dataset(filepath, "r", format="NETCDF4")

    datas = {}
    units = []
    for v in f.variables.keys():
        new_v = v
        if v == "latitude":
            new_v = "lat"
        if v == "longitude":
            new_v = "lon"
        datas[new_v] = (f.variables[v][:].tolist())
        print(f.variables[v].units)
        units.append([v, f.variables[v].units])
    datas["units"] = units
    f.close()

    data_json = json.dumps(datas, sort_keys=True)

    return data_json


#
# path = '../stations/CGR/'
# files = []
# for file in os.listdir(path):
#     if file.endswith(".nc"):
#         files.append(file)
#
# for f in files:
#     test = json_from_netcdf_file("../stations/CGR/" + f)
#     json_f = f.replace(".nc", ".json")
#     with open("../stations/CGR/" + json_f, 'w') as outfile:
#         outfile.write(test)

# with open("../stations/CGR/"+files[0].replace(".nc",".json")) as file:
#     data = json.load(file)

# print(data)

# test = json_from_netcdf_file("../stations/CGR/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")
# print(len(test["latitude"][0]))
