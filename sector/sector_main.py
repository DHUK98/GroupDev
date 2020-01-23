"""
Sector trajectories based on parameters
"""


import sys, json
sys.path.insert(1, '../utils')    # allow reading of utils functions

from json_reader import json_from_netcdf_file
import math






"""
Take in JSON.. done
    Use utils folder function.. done

Iterate through each trajectory's points
Check if the lat/lon is in the sector based on parameters
    Think about graph, the sector and the trajectories are using a common scale

    Have a count that increments each time it is not in the sector
    if it gets to 5 or 6 not in the sector then disregard the sector and move on to the next
        assign a new JSON and delete the entry off of that one so that the iterating still works
    if you get to the end then add that trajectory to another JSON in the same format 

"""

def sector(data, start_angle, end_angle, start_lat, start_lon):
    start_angle_r = math.radians(start_angle)
    end_angle_r = math.radians(end_angle)
    print("Running with start angle " + str(start_angle) + " and end angle " + str(end_angle))

    print(len(data['lat']))

    # for each trajectory
    for t in range(len(data['lat'])):

        lats = data['lat'][t]
        lons = data['lon'][t]

        # for each point, work out angle from centre
        #  we need if statements for the four segments out from the circle

        out_count = 0
        for l in range(len(lats)):

            if not check_point(lons[l] - start_lon, lats[l] - start_lat, start_angle_r, end_angle_r):
                out_count += 1
            else:
                print("\nPoint (" + str(lats[l]) + ", " + str(lons[l]) + ") lies in sector")
                pass
            if out_count > 5:
                print("Trajectory discarded due to high out count")
                """
                Delete trajectory from JSON after N counts outside the sector
                """
                break

            # if l == len(lats):
            #     print("\n**\nTrajectory ")
        out_count = 0

    sectored_data = data
    return sectored_data


def check_point(x, y, start_angle, end_angle):
    # print("Checking point with adjusted longitude " + str(x), end="")
    # print(" and with adjusted latitude " + str(y))
    if x != 0:
        angle = math.atan(y / x)
    else:
        angle = math.atan(math.inf)
    print("Checking angle " + str(math.degrees(angle)))

    if angle >= start_angle and angle <= end_angle:
        return True
    else:
        # print("point does not exist in circle sector")
        return False
    pass



if __name__ == "__main__":
    example_path = "../data/ERA-Interim_1degree_CapeGrim_100m_2012_hourly.nc"
    example_lat = -40.682
    example_lon = 144.688

    print("Loading data...", end="")
    example_data = json.loads(json_from_netcdf_file(example_path))
    print("Done")
    output_data = sector(example_data, start_angle=30, end_angle=180, start_lat=example_lat, start_lon=example_lon)
