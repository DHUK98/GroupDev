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


import sys, json, math
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(1, '../utils')    # allow reading of utils functions

from json_reader import json_from_netcdf_file



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


            # - 190 -> 170
            #(-190) + 360 = 170

            # if traj_lon_from_center > 180 or traj_lon_from_center < -180:
            if abs(traj_lat_from_center - last_lat) > 90:
                # print("Anomalous Lat")
                # print("Lat: ", end="")
                # print(traj_lat_from_center)
                # print("Lon: ", end="")
                # print(traj_lon_from_center)

                # print("Changing lat from " + str(traj_lat_from_center) + " to " + str(traj_lat_from_center + 180), end="\n\n")
                traj_lat_from_center += 180


            if abs(traj_lon_from_center - last_lon) > 180:
                # print("Anomalous Lon")
                # print("Lat: ", end="")
                # print(traj_lat_from_center)
                # print("Lon: ", end="")
                # print(traj_lon_from_center)
                # print("lons were wrong")
                # change lon
                traj_lon_from_center += 360





            #     pass
            #     print("Adding 360 to lon")
            #     traj_lon_from_center += 360


                # continue


            traj_lats.append(traj_lat_from_center)
            traj_lons.append(traj_lon_from_center)

            # print(traj_lat_from_center)
            # print(traj_lon_from_center)

            # ax.add_artist(circle)

            # if not check_point(lons[l] - start_lon, lats[l] - start_lat, start_angle_r, end_angle_r):
            #     out_count += 1
            # else:
            #     # print("\nPoint (" + str(lats[l]) + ", " + str(lons[l]) + ") lies in sector")
            #     pass
            # if out_count > 5:
            #     break

            if l >= (len(lats) - 1):
                # print("Got to last hour")
                # print("\n**\nTrajectory included!")
                #
                # sectored_data['time'].append(data['time'][t])
                # sectored_data['lat'].append(data['lat'][t])
                # sectored_data['lon'].append(data['lon'][t])
                # sectored_data['height'].append(data['height'][t])
                # sectored_data['pressure'].append(data['pressure'][t])

                # print("*", end="")
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



if __name__ == "__main__":
    example_path = "../data/ERA-Interim_1degree_CapeGrim_100m_2012_hourly.nc"
    example_lat = -40.682
    example_lon = 144.688

    print("Loading data...", end="")
    example_data = json.loads(json_from_netcdf_file(example_path))
    print("Done")
    output_data = sector(example_data, start_angle=0, end_angle=360, start_lat=example_lat, start_lon=example_lon)
    print("\n\n\nOUTPUT DATA: ")
    print(output_data)