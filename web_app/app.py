from flask import Flask, render_template
import os
import json
import sys
import json
from flask import jsonify
from static.utils.json_reader import json_from_netcdf_file
import pprint

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
    data = json.loads(json_from_netcdf_file('static/stations/CGR/UKESM_1degree_CapeGrim_100m_2012_hourly.nc'))
    lat_lon = []
    for i in range(len(data["lat"])):
        lat_lon.append([data["lat"][i], data["lon"][i]])
    print(lat_lon[0])
    lat_lon2 = []
    for j in range(len(lat_lon)):
        cur = lat_lon[j]
        temp = []
        for k in range(len(cur[0])):
            temp.append([cur[0][k],cur[1][k]])
        lat_lon2.append(temp)
    print(lat_lon2[0])
    lat = 0
    lng = 0
    try:
        with open('static/stations/' + iid + "/info.json") as json_file:
            data = json.load(json_file)
            lat = data["lat"]
            lng = data["lon"]
            name = data["Station"]
        return render_template('station_view.html', id=iid, lat=lat, lng=lng, name=name, test_traj=lat_lon2)
    except Exception as e:
        return str(e)


@app.route('/sector/<iid>/<start_ang>/<end_ang>/<dist>/<thresh>')
def sector(iid, start_ang, end_ang, dist, thresh):
    # return jsonify("OUT: " + str(iid + " " + start_ang + " "+ end_ang + " " +dist +" "+ thresh))
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/", "cluster.json")
    data = json.load(open(json_url))
    return data


@app.route('/cluster/<iid>/')
def cluster(iid):
    # return jsonify("OUT: " + str(iid + " " + start_ang + " "+ end_ang + " " +dist +" "+ thresh))
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/", "cluster.json")
    data = json.load(open(json_url))
    return jsonify(data)


if __name__ == '__main__':
    app.run()
