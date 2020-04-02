import gzip
import os
from collections import Counter
from os.path import join, dirname, realpath

import ujson as json
from flask import Flask, render_template, request, session
from flask import jsonify, make_response
from flask_session import Session

import utils.sector as sec
from utils.cluster import cluster_request
from utils.data_manager import apply_mask, get_datas as gds, list_files, get_keys
from utils.json_to_netcdf import json_to_netcdf
from utils.median_calc import get_median_colours
from utils.zip_netcdf import zip_netcdf_exports, delete_nc_exports

from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = '\ni-\x9e\xd2\xc2\xf4%\xa8\xa0\x99\xa1\xd5z\x05\xb9\xca\x0fQ\x04\xa0\xe6v\x81'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

STATIC_PATH = Path(join(dirname(realpath(__file__)), 'static'))


@app.route('/')
def home():
    json_url = join(STATIC_PATH, 'stations.json')
    data = json.load(open(json_url))
    return render_template('station_selector.html', stations=data)


@app.route("/load_data/<id>/", methods=['POST'])
def load_data(id):
    print("LOAD DATA")
    data = request.get_json()
    path = join(STATIC_PATH, "stations/" + id + "/")
    data = data[0]
    session["data"] = json.dumps(gds(path, data))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/station/<iid>')
def station(iid):
    path = STATIC_PATH / "stations" / iid
    file_ns = list_files(path, with_path=False)

    for f in range(len(file_ns)):
        temp = file_ns[f]
        split = temp.split("_")
        file_ns[f] = split[0] + " " + split[-2]

    keys = get_keys(path)
    print(keys)

    with open(path / "info.json") as json_file:
        data = json.load(json_file)
        lat = data["lat"]
        lng = data["lon"]
        name = data["Station"]

    return render_template('station_view.html', id=iid, lat=lat, lng=lng, name=name, file_ns=file_ns, keys=keys)


@app.route('/cluster/req/<iid>/<min_samp>/<eps_val>', methods=['POST'])
def cluster_dbscan(iid, min_samp, eps_val):
    data = request.get_json()
    filepath = data[1]

    mask = json.loads(data[0])
    f_name = data[1]

    with open("static/stations/" + iid + "/" + f_name, "r") as f:
        traj_full = json.load(f)
    traj = apply_mask(mask, traj_full)

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
    mask = request.get_json()
    # print(data)
    data = json.loads(session.get("data"))
    data = apply_mask(mask, data)

    # K-means request
    cluster = cluster_request(json.dumps(data), cluster_type="kmeans", cluster_no=n)
    cluster_json = json.loads(cluster)
    print(cluster_json["labels"])

    print(len(cluster_json["labels"]))
    return jsonify(cluster)


@app.route('/convert_to_netcdf/<index_json>', methods=['POST'])
def convert_to_netcdf(index_json):
    data = request.get_json()
    json_to_netcdf(data, "cluster_" + str(int(index_json) + 1))
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/zip_netcdf_exports', methods=['POST'])
def zip_netcdf():
    zip_netcdf_exports()
    delete_nc_exports()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/sector/<id>/<int:i>/<int:start_ang>/<int:end_ang>/<int:dist>/<int:thresh>')
def sector(id, i, start_ang, end_ang, dist, thresh):
    return jsonify(sec.sector(id, i, start_ang, end_ang, dist, thresh))


@app.route('/filter/<id>/<int:i>/<var>/<int:min>/<int:max>/<int:thresh>')
def filter(id, i, var, min, max, thresh):
    return jsonify(sec.filter(id, i, var, min, max, thresh))


@app.route('/getdata/<id>', methods=['POST'])
def get_data(id):
    print("get data")
    mask = request.get_json()[0]
    keys = []
    if request.get_data()[1]:
        keys = request.get_json()[1]
    print("mask loaded")
    data = json.loads(session.get("data"))
    rem = []
    for d in data.keys():
        if d not in keys:
            rem.append(d)
    for r in rem:
        del data[r]
    out = json.dumps(apply_mask(mask, data))
    print("get data done")
    content = gzip.compress(out.encode('utf8'), 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    print(response)
    return response


if __name__ == '__main__':
    app.run()
