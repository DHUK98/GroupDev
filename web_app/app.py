from flask import Flask, render_template
import os
import json
import sys
from flask import jsonify

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
    lat = 0
    lng = 0
    try:
        with open('static/stations/' + iid + "/info.json") as json_file:
            data = json.load(json_file)
            lat = data["lat"]
            lng = data["lon"]
            name = data["Station"]
        print(lat, lng)
        return render_template('station_view.html', id=iid, lat=lat, lng=lng, name=name);
    except Exception as e:
        return str(e)


@app.route('/sector/<iid>/<start_ang>/<end_ang>')
def sector(iid, start_ang, end_ang):
    return jsonify(str(iid + start_ang + end_ang));


if __name__ == '__main__':
    app.run()
