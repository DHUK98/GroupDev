from flask import Flask, render_template, request
import os
import json
import sys
import json
from flask import jsonify
import os
from static.utils.cluster import linkage_request, h_cluster_request

sys.path.insert(1, '../sector')
# from sector_main import sector

app = Flask(__name__)


@app.route('/')
def home():
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, 'static', 'stations.json')
    data = json.load(open(json_url))
    return render_template('station_selector.html', stations=data)


@app.route('/station/<iid>')
def station(iid):
    try:
        path = 'static/stations/' + iid + "/"
        file_ns = []
        for file in os.listdir(path):
            if file.startswith("info"):
                continue
            if file.endswith(".json"):
                file_ns.append(file)

        with open(path + "info.json") as json_file:
            data = json.load(json_file)
            lat = data["lat"]
            lng = data["lon"]
            name = data["Station"]
        return render_template('station_view.html', id=iid, lat=lat, lng=lng, name=name, file_ns=file_ns)
    except Exception as e:
        return str(e)


@app.route('/cluster/req/<iid>', methods=['POST'])
def cluster(iid):
    data = request.get_json()
    print(data)
    mask = json.loads(data[0])
    f_name = data[1]
    print(data)
    with open("static/stations/" + iid + "/" + f_name, "r") as f:
        traj = json.load(f)
    traj = applyMask(mask, traj)
    print(len(traj["lon"]))
    linkage = linkage_request(json.dumps(traj))
    cluster = h_cluster_request(json.dumps(traj),linkage,15)
    print(cluster)
    return jsonify(cluster)


def applyMask(mask, d):
    d = json.loads(json.dumps(d))

    lat = d["lat"]
    lon = d["lon"]
    time = d["time"]
    height = d["height"]
    pressure = d["pressure"]

    n_lat = []
    n_lon = []
    n_time = []
    n_height = []
    n_pressure = []

    for i in range(len(mask)):
        if mask[i] == 1:
            n_lat.append(lat[i])
            n_lon.append(lon[i])
            n_time.append(time[i])
            n_height.append(height[i])
            n_pressure.append(pressure[i])

    out = {"lat": n_lat,
           "lon": n_lon,
           "time": n_time,
           "height": n_height,
           "pressure": n_pressure}

    return out


#     }
#     let json = {
#         "lat": n_lat,
#         "lon": n_lon,
#         "time": n_time,
#         "height": n_height,
#         "pressure": n_pressure
#     };
#
#     return JSON.stringify(json);
# }


if __name__ == '__main__':
    app.run()
