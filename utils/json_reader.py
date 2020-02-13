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
    # print(f)

    print(f.variables['latitude'])
    print(f.variables['longitude'])
    # print()
    # for v in f.groups:
    #     print(v)


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
    data_dict = {"time" : time.tolist(), "lat" : lat.tolist(), "lon" : lon.tolist(), "height" : height.tolist(), "pressure" : pressure.tolist()}
    data_json = json.dumps(data_dict, sort_keys=True)

    f.close()

    return data_json


if __name__ == "__main__":
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "..\\data\\ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")
    json_output = json_from_netcdf_file("D:\\PrototypeNovClim\\GroupDev\\data\\ERA-Interim_1degree_CapeGrim_100m_2012_hourly.nc")
    with open("json_test.json", "w+") as fw:
        json.dump(json_output, fw)

