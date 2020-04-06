import matplotlib.pyplot as plt
from flask import session
import ujson as json


def plot_svg():
    """ renders the plot on the fly.
    """
    fig = plt.figure(figsize=(4, 4))
    data = json.loads(session.get("data"))
    xs = []
    ys = []
    for i in range(0, 600, 100):
        ys.append(data["height"][i])
        xs.append(range(240, -1, -1))
    plt.xlabel("Time (Hours)")
    plt.ylabel("Height")

    for j in range(len(xs)):
        plt.plot(xs[j], ys[j],label="cluster " + str(j+1))
    plt.tight_layout()
    plt.legend()
    return fig
