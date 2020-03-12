from flask import Flask, render_template, request
import json
from flask import jsonify
import os
from collections import Counter
from static.utils.cluster import linkage_request, cluster_request, cluster_request_dbscan, dbscan_kmeans
from static.utils.json_to_netcdf import json_to_netcdf
from static.utils.zip_netcdf import zip_netcdf_exports, delete_nc_exports
from static.utils.median_calc import get_median_colours

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
        path = "static/stations/" + iid + "/"
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


# DBSCAN
@app.route('/cluster/req/<iid>/<min_samp>/<eps_val>', methods=['POST'])
def cluster_dbscan(iid, min_samp, eps_val):
    data = request.get_json()
    filepath = data[1]
    print("DATA FILEPATH IS ", end="")
    print(filepath)

    mask = json.loads(data[0])
    f_name = data[1]

    with open("static/stations/" + iid + "/" + f_name, "r") as f:
        traj_full = json.load(f)
    traj = applyMask(mask, traj_full)

    print("Sample Traj_Full:")
    for i in range(5):
        print(traj_full["lat"][i])
    # print(traj_full)
    print("Of length: " + str(len(traj_full["lat"])))

    print("Sample Traj:")
    for i in range(5):
        print(traj["lat"][i])
    # print(traj)
    print("Of length: " + str(len(traj["lat"])))

    print("There are this many of traj: " + str(len(traj['lat'])))

    # cluster = cluster_request_dbscan(json_msg=json.dumps(traj), min_samples=int(min_samp), eps=float(eps_val))
    # cluster = dbscan_kmeans(json.dumps(traj), 10, 10, 150)

    cluster = cluster_request(json.dumps(traj), cluster_type='dbscan', min_samples=int(min_samp), eps=int(eps_val))
    cluster_json = json.loads(cluster)
    centroid_sizes = Counter(cluster_json['labels'])
    print("\n\nThere are " + str(len(centroid_sizes) - 1) + " centroid trajectories")
    print("\nWeights: ")
    print(sorted(centroid_sizes.items()))

    # currently for height, not parameter
    c_colours = get_median_colours(traj, cluster_json['labels'], "height")
    print(c_colours)

    cluster_json["colours"] = c_colours
    cluster = json.dumps(cluster_json)
    return jsonify(cluster)


# K-Means
@app.route('/cluster/req/<iid>/<n>', methods=['POST'])
def cluster(iid, n):
    data = request.get_json()
    # print(data)
    mask = json.loads(data[0])
    f_name = data[1]
    # print(data)
    with open("static/stations/" + iid + "/" + f_name, "r") as f:
        traj = json.load(f)
    traj = applyMask(mask, traj)

    # K-means request
    cluster = cluster_request(json.dumps(traj), cluster_type="kmeans", cluster_no=n)
    cluster_json = json.loads(cluster)
    print(cluster_json["labels"])

    print(len(cluster_json["labels"]))
    print(len(data[0]))


    # currently for height, not parameter
    c_colours = get_median_colours(traj, cluster_json['labels'], "height")
    print(c_colours)

    cluster_json["colours"] = c_colours
    # cluster = json.dumps(cluster_json)

    return jsonify(cluster)


@app.route('/convert_to_netcdf/<index_json>', methods=['POST'])
def convert_to_netcdf(index_json):
    data = request.get_json()
    json_to_netcdf(data, "cluster_" + str(int(index_json) + 1))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/zip_netcdf_exports', methods=['POST'])
def zip_netcdf():
    print("ZIP NETCDF APP FUNCTION")
    zip_netcdf_exports()
    delete_nc_exports()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


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


if __name__ == '__main__':
    app.run()
