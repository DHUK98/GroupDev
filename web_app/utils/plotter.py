import io

from matplotlib.figure import Figure

from flask import session
import ujson as json

def plot_svg():
    """ renders the plot on the fly.
    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    data = json.loads(session.get("data"))
    ys = data["height"][0]
    xs = data["time"][0]

    axis.plot(xs, ys)
    return fig