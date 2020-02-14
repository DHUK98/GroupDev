'''
Module for converting data to/from json
'''

from netCDF4 import Dataset
import os.path
import pprint
import json


def json_from_netcdf_file(filepath):
    """
    First part is from old reader.py file.
    We can either replace that with a call to the initialise function in reader
    or just use these util files and render reader.py obsolete
    """

    f = Dataset(filepath, "r", format="NETCDF4")
    print(f.dimensions)

    # # read in variables
    mt = f.variables['time']
    try:
        lat = f.variables['latitude']
        lon = f.variables['longitude']
    except:
        lat = f.variables['lat']
        lon = f.variables['lon']

    height = f.variables['height']
    pressure = f.variables['pressure']

    time = mt[:]
    lat = lat[:]
    lon = lon[:]
    height = height[:]
    pressure = pressure[:]

    # .tolist() function takes a few seconds but is needed to make the np.MaskedArray type JSON serialisable
    data_dict = {"time": time.tolist(), "lat": lat.tolist(), "lon": lon.tolist(), "height": height.tolist(),
                 "pressure": pressure.tolist()}
    data_json = json.dumps(data_dict, sort_keys=True)

    f.close()
    return data_json


# path = '../stations/CGR/'
# files = []
# for file in os.listdir(path):
#     if file.endswith(".nc"):
#         files.append(file)
# #
# # for f in files:
# #     test = json_from_netcdf_file("../stations/CGR/" + f)
# #     json_f = f.replace(".nc", ".json")
# #     with open("../stations/CGR/" + json_f, 'w') as outfile:
# #         outfile.write(test)
#
# with open("../stations/CGR/"+files[0].replace(".nc",".json")) as file:
#     data = json.load(file)
#
# print(data)


