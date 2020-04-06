import io

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from flask import session
import ujson as json


def plot_svg():
    """ renders the plot on the fly.
    """
    fig, axs = plt.subplots(2, 3,figsize=(15,10))
    data = json.loads(session.get("data"))
    xs = []
    ys = []
    for i in range(0,600,100):
        ys.append(data["height"][i])
        xs.append(data["time"][i])

    for i in range(2):
        for j in range(3):
            axs[i, j].set_title('Cluster ' + str(i+j))
            axs[i, j].plot(xs[i+j], ys[i+j])

    fig.tight_layout(pad=2.5)

    for ax in axs.flat:
        ax.set(xlabel='time', ylabel='heigt')
    return fig
