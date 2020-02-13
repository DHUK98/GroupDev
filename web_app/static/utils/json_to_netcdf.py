from netCDF4 import Dataset
import json
import numpy as np
from json_reader import json_from_netcdf_file

def json_to_netcdf(json_filepath):
    keys = []

    # load json from filepath
    with open(json_filepath) as f:
        json_data = json.load(f)

    # create new netCDF file
    nc_file = Dataset("test.nc", "w", format="NETCDF4")

    # # iterate through keys
    # for (k, v) in json_data.items():
    #     keys.append(k)
    #     print("Key: " + str(k))


    # create metadata
    nc_file.title = 'Exported data'
    nc_file.author = "Dennis Harrop, Max Weeden and Hugo Wickham " \
                     "\nUniversity of Exeter ECMM427 Group Development Project Module"

    # create dimensions of trajectory_number and time
    nc_file.createDimension("trajectory_number", 8757)
    nc_file.createDimension("time", 241)

    # create variables
    time = nc_file.createVariable("time", 'd', ('trajectory_number', 'time',))
    lat = nc_file.createVariable("lat", 'd', ('trajectory_number', 'time',))
    lon = nc_file.createVariable("lon", 'd', ('trajectory_number', 'time',))
    height = nc_file.createVariable("height", 'u8', ('trajectory_number', 'time',))
    pressure = nc_file.createVariable("pressure", 'd', ('trajectory_number', 'time',))


    time[:] = json_data['time']
    lat[:] = json_data['lat']
    lon[:] = json_data['lon']
    height[:] = json_data['height']
    pressure[:] = json_data['pressure']

    # print("-- Wrote data, lat.shape is now ", lat.shape)

    nc_file.close()


if __name__ == "__main__":
    print("Running")

    json_to_netcdf("../stations/CGR/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.json")
    data_check = json_from_netcdf_file("test.nc")
    data_check = json.loads(data_check)

    for i in range(10):
        print(data_check['lat'][i])

