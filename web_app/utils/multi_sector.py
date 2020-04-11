from pyproj import Transformer
import math
from flask import session
import numpy as np


def angle_between_points(p1_x, p1_y, p2_x, p2_y):
    out = math.atan2(p2_y - p1_y, p2_x - p1_x) * 180 / math.pi
    return out


def is_angle_between(n, a, b):
    n = (360 + (n % 360)) % 360
    a = (3600000 + a) % 360
    b = (3600000 + b) % 360

    if a < b:
        return a <= n <= b
    return a <= n or n <= b


def sector_point(x, y, start_ang, end_ang, dist):
    point_ang = 360 - angle_between_points(0, 0, x, y) + 90
    a = 0 - x
    b = 0 - y
    d = math.sqrt(a * a + b * b)
    if d > dist:
        return False
    return is_angle_between(point_ang, start_ang, end_ang)


def sector(id, i, start_ang, end_ang, dist, thresh):
    print("sector.py sector start")
    output = []
    # data = get_data(id, i)
    data = session.get('data')
    lat = data["lat"]
    lon = data["lon"]
    transformer = Transformer.from_crs({"proj": "longlat", "datum": 'WGS84'},
                                       {"proj": 'aeqd', "lon_0": str(lon[0][0]), "lat_0": str(lat[0][0]),
                                        "datum": 'WGS84'}, skip_equivalent=True)
    if start_ang == 0 and end_ang == 360:
        return list(np.ones(len(lat)))

    print("start loop")
    for j in range(len(lat)):
        outside = 0
        for k in range(len(lat[j])):
            if outside > thresh:
                break
            test = transformer.transform(np.array(lon[j][k]), np.array(lat[j][k]))
            sec = sector_point(test[0], test[1], start_ang, end_ang, dist)
            if not sec:
                outside += 1

        if outside <= thresh:
            output.append(1)
        else:
            output.append(0)

    print("sector.py sector done")

    return output


def filter(id, i, var, min, max, thresh):
    data = session.get('data')[var]
    r = []
    for j in range(len(data)):
        cur_traj = data[j]
        out = 0
        for k in range(len(cur_traj)):
            if cur_traj[k] > max or cur_traj[k] < min:
                out += 1
            if out > thresh:
                r.append(0)
                break
        if out <= thresh:
            r.append(1)
    return r
