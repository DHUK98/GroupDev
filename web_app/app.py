from flask import Flask, render_template
import os
import json
from flask import request

app = Flask(__name__)


@app.route('/')
def home():
    site_root = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(site_root, 'static', 'stations.json')
    data = json.load(open(json_url))
    return render_template('station_selector.html', stations=data)


@app.route('/station/<iid>')
def station(iid):
    return render_template('station_view.html', id=iid);


if __name__ == '__main__':
    app.run()
