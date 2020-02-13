"""
Sector trajectories based on parameters
"""

"""
{
time : [1, 2, 3], [1, 2, 3], [2, 3, 4]
lat : [1, 2, 3], etc.. 
lon : 
height :
pressure : 

}


"""


import sys, json, math, operator
from matplotlib.path import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
sys.path.insert(1, '../utils')    # allow reading of utils functions

from json_reader import json_from_netcdf_file


"""
Currently: 
Drawing polygon, making all points relative to the sensor origin
Checking if points fall inside the polygon
This works, however the translation of points does not take into account the wrapping around at edges
from -170 to 170 lat for example. This is only a 20 degree difference 
but will not translate towards the new relative origin correctly because of the pos/neg signs etc

Need to do/fix:
A better way would be to use some other conversion package to convert lat/lon to x/y
So we won't have to think about it
Look at latlon_to_xy_conversion_example.py in same folder for what I'm attempting to do
But I can't get pyproj to install for the life of me
If someone could install pyproj and try running it that would be great
You need to install this proj Windows binary and I've done everything but nada
It might end up being easier on Mac 

Failing that try basemap, 
it's not as targeted towards just converting coordinates but it has the functionality
though I also can't seem to get the sodding thing to install for the same reason
"""

# pass lat lon coordinates of polygon points
# unpack tuple, don't change tuple
# just unpack and change points when making polygon
def polygon_sector(data, points, start_lat, start_lon, interpolation=False):
    sectored_data = dict()
    r_start_lat = 0
    r_start_lon = 0
    contains_count = 0
    doesnt_contain_count = 0
    # Create polygon
    r_polygon = create_polygon(start_lat, start_lon, points)

    for t in range(len(data['lat'])):

        lats = data['lat'][t]
        lons = data['lon'][t]

        for l in range(len(lats)):

            new_lat = lats[l]
            new_lon = lons[l]

            r_lat = lats[l] - start_lat
            r_lon = lons[l] - start_lon

            if r_polygon.contains_point(tuple((r_lat, r_lon))):
                # print("It contains : (" + str(r_lat) + ", " + str(r_lon) + ")")
                contains_count += 1
            else:
                # print("It doesn't contains : (" + str(r_lat) + ", " + str(r_lon) + ")")
                doesnt_contain_count += 1

        if contains_count > 1:
            print("\n\nTrajectory " + str(t) + ": ")
            print("In sector: " + str(contains_count) + " hours")
            print("Not in sector: " + str(doesnt_contain_count) + " hours")

        contains_count = 0
        doesnt_contain_count = 0


def create_polygon(start_lat, start_lon, points):
    # create polygon relative to sensor from lat/lon points
    r_point_list = []
    # print(points)

    for p in points:
        (lat, lon) = p
        r_point_list.append(tuple((lat - start_lat, lon - start_lon)))

    # join up path with first point again to complete polygon
    point = points[0]
    (lat, lon) = point
    r_point_list.append(tuple((lat - start_lat, lon - start_lon)))

    # append codes to draw polygon
    codes = []
    codes.append(Path.MOVETO)
    for i in range(len(points) - 1):
        codes.append(Path.LINETO)
    codes.append(Path.CLOSEPOLY)

    print("Verts:")
    for r_point in r_point_list:
        print(r_point)

    r_polygon = Path(r_point_list, codes)

    # plot poly for fun
    fig, ax = plt.subplots()
    patch = patches.PathPatch(r_polygon, facecolor='orange', lw=2)
    ax.add_patch(patch)
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    plt.show()

    return r_polygon



def sector(data, start_angle, end_angle, start_lat, start_lon):

    line_count = 0

    sectored_data = dict()
    start_angle_r = math.radians(start_angle)
    end_angle_r = math.radians(end_angle)
    print("Running with start angle " + str(start_angle) + " and end angle " + str(end_angle))
    print("Length of data before sectoring: " + str(len(data['lat'])))
    print(len(data['lat']))


    # for each trajectory
    for t in range(len(data['lat'])):
        last_lat = 0
        last_lon = 0

        traj_lats = []
        traj_lons = []

        lats = data['lat'][t]
        lons = data['lon'][t]

        out_count = 0
        for l in range(len(lats)):

            traj_lat_from_center = lats[l]
            traj_lon_from_center = lons[l]

            # if traj_lon_from_center > 180 or traj_lon_from_center < -180:
            if abs(traj_lat_from_center - last_lat) > 90:

                # print("Changing lat from " + str(traj_lat_from_center) + " to " + str(traj_lat_from_center + 180), end="\n\n")
                traj_lat_from_center += 180


            if abs(traj_lon_from_center - last_lon) > 180:

                traj_lon_from_center += 360

            traj_lats.append(traj_lat_from_center)
            traj_lons.append(traj_lon_from_center)

            if l >= (len(lats) - 1):    # final hour
                plt.plot(traj_lons, traj_lats, color='k', linestyle='-', linewidth=0.5)
                last_lat = traj_lat_from_center
                last_lon = traj_lon_from_center
    plt.show()

    print("\n\nLength of data after sectoring: " + str(len(data['lat'])))

    return sectored_data


def check_point(x, y, start_angle, end_angle):
    # print("Checking point with adjusted longitude " + str(x), end="")
    # print(" and with adjusted latitude " + str(y))
    # x = x / 2
    if x != 0:
        angle = math.atan(y / x)
    else:
        angle = math.atan(math.inf)
    # print("Checking angle " + str(math.degrees(angle)))

    if angle >= start_angle and angle <= end_angle:
        return True
    else:
        # print("point does not exist in circle sector")
        return False
    pass


def filter_attr_single(attr, threshold, threshold_time, greater_or_lesser):
    # Function to filter out a single trajectory whose attribute oversteps the threshold
    # at least threshold_time number of times
    # height -> list containing height measurements over time for single trajectory
    # threshold -> maximum permitted value for height
    # threshold_time -> amount of time in hours the trajectory is allowed to spend above the threshold
    # Returns True if the trajectory is permitted, False if trajectory is to be discarded
    count = 0

    if greater_or_lesser == operator.gt:         # check if each is over threshold

        for a in attr:
            if a > threshold:       # greater than
                count += 1
            if count > threshold_time:
                return False

    else:                                       # check if each is under threshold
        for a in attr:
            if a < threshold:               # less than
                count += 1
            if count > threshold_time:
                return False

    return True


def filter_attr(attrs, threshold, threshold_time, greater_or_lesser):
    # Function to apply filter_height_single() to whole set of measurements
    # heights -> list containing height measurements over time for all trajectories
    # threshold -> maximum permitted value for height
    # threshold_time -> amount of time the trajectory is allowed to spend above the threshold

    filtered_attrs = []

    for attr in attrs:
        if filter_attr_single(attr, threshold, threshold_time, greater_or_lesser):
            filtered_attrs.append(attr)

    return filtered_attrs


if __name__ == "__main__":
    example_path = "../data/ERA-Interim_1degree_CapeGrim_100m_2012_hourly.nc"
    example_lat = -40.682
    example_lon = 144.688
    example_points = [(-40.682, 144.688), (-35.682, 144.38), (-35.682, 138.688)]

    print("Loading data...", end="")
    example_data = json.loads(json_from_netcdf_file(example_path))
    print("Done")
    output_data = polygon_sector(example_data, points=example_points, start_lat=example_lat, start_lon=example_lon)
    print("\n\n\nOUTPUT DATA: ")
    print(output_data)