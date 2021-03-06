import gzip
import io
from os.path import join, dirname, realpath

import ujson as json
from copy import copy
from flask import Flask, render_template, request, session, jsonify, make_response, Response, send_file
from flask_session import Session

import utils.sector as sec
from utils.cluster import cluster_request
from utils.data_manager import apply_mask, get_datas, list_files, get_keys
from utils.json_to_netcdf import json_to_netcdf
from utils.median_calc import get_median_colours
from utils.zip_netcdf import zip_netcdf_exports, delete_nc_exports
from matplotlib.backends.backend_svg import FigureCanvasSVG
import utils.plotter as plotter

app = Flask(__name__)
app.config['SECRET_KEY'] = '\ni-\x9e\xd2\xc2\xf4%\xa8\xa0\x99\xa1\xd5z\x05\xb9\xca\x0fQ\x04\xa0\xe6v\x81'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

STATIC_PATH = join(dirname(realpath(__file__)), 'static')


# Station selector
@app.route('/')
def home():
    json_url = join(STATIC_PATH, 'stations.json')
    station_data = json.load(open(json_url))
    return render_template('station_selector.html', stations=station_data)


# Load data by station id and index's of files to load
@app.route("/load_data/<id>/", methods=['POST'])
def load_data(id):
    indexs = request.get_json()[0]
    path_to_station = join(STATIC_PATH, "stations", id)

    data, keys = get_datas(path_to_station, indexs)
    session["data"] = data
    session["keys"] = json.dumps(keys)
    return jsonify(session.get("keys"))


@app.route("/keys")
def getkeys():
    return jsonify(session.get("keys"))


@app.route("/plot_figure", methods=["POST"])
def plot_figure():
    data = request.get_json()

    keys = list(data[0])
    num_clusters = int(data[1])
    mask = list(data[2])

    full_data = session.get("data")
    print(len(full_data["lat"]))
    masked_data = apply_mask(mask, full_data)
    print(len(masked_data["lat"]))
    clustered_data = cluster_request(masked_data, keys, cluster_type="kmeans", cluster_no=num_clusters)
    centroids = list(clustered_data["centroids"])
    count = list(clustered_data["count"])

    if len(keys) <= 2:
        fig = plotter.plot_svg(centroids, keys, count)
    else:
        fig = plotter.plot_svg3d(centroids, keys, count)

    output = io.StringIO()
    fig.savefig(output, format='svg')
    output.seek(0)  # rewind the data
    val = '<svg' + output.getvalue().split('<svg')[1]
    r = Response(val, mimetype="html")
    return r


@app.route('/station/<iid>')
def station(iid):
    path_to_station = join(STATIC_PATH, "stations", iid)

    file_names = list_files(path_to_station, with_path=False)

    # Filter file name to just source and year
    for file in range(len(file_names)):
        file_name = file_names[file]
        split = file_name.split("_")
        file_names[file] = split[0] + " " + split[-2]

    data_keys = get_keys(path_to_station)

    # Load information about current station
    with open(join(path_to_station, "info.json")) as json_file:
        data = json.load(json_file)
        lat = data["lat"]
        lon = data["lon"]
        name = data["Station"]

    return render_template('station_view.html', id=iid, lat=lat, lon=lon, name=name, file_ns=file_names, keys=data_keys)


@app.route('/cluster/req/<iid>/<min_samp>/<eps_val>', methods=['POST'])
def cluster_dbscan(iid, min_samp, eps_val):
    mask = request.get_json()

    full_data = session.get("data")
    masked_data = apply_mask(mask, full_data)

    clustered_data = cluster_request(json.dumps(masked_data), ["lat", "lon"], cluster_type='dbscan',
                                     min_samples=int(min_samp),
                                     eps=int(eps_val))

    return jsonify(clustered_data)


# K-Means
@app.route('/cluster/req/<iid>/<n>', methods=['POST'])
def cluster(iid, n):
    mask = request.get_json()
    # print(data)
    full_data = session.get("data")
    masked_data = apply_mask(mask, full_data)

    # K-means request
    clustered_data = cluster_request(masked_data, ["lat", "lon"], cluster_type="kmeans", cluster_no=n)
    clustered_data = json.dumps(clustered_data)
    return jsonify(clustered_data)


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
    data = session.get("data")
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
