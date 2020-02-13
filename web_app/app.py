from flask import Flask, render_template
import os
import json
import sys
import json
from flask import jsonify
import os
from static.utils import  cluster

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


@app.route('/cluster/<num_c>', methods=['GET', 'POST'])
def cluster(iid,num_c):
    cluster.h_cluster_request(,num_c)
    return ""


if __name__ == '__main__':
    app.run()
