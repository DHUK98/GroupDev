'''
Module for converting data to/from json
'''

from netCDF4 import Dataset
import os.path
import json


def json_from_netcdf_file(filepath):
    """
    First part is from old reader.py file.
    We can either replace that with a call to the initialise function in reader
    or just use these util files and render reader.py obsolete
    """

    f = Dataset(filepath, "r", format="NETCDF4")

    # # read in variables
    mt = f.variables['time']
    lat = f.variables['latitude']
    lon = f.variables['longitude']
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
