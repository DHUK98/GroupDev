import matplotlib.pyplot as plt
from flask import session
import ujson as json


def plot_svg(data):
    """ renders the plot on the fly.
    """
    fig = plt.figure(figsize=(4, 4))
    xs = []
    ys = data[0]
    for i in range(6):
        xs.append(range(240, -1, -1))
    plt.xlabel("Time (Hours)")
    plt.ylabel("Height")

    for j in range(len(xs)):
        plt.plot(xs[j], ys[j], label="cluster")
    plt.tight_layout()
    plt.legend()
    return fig


def plot_svg3d(data, count):
    """ renders the plot on the fly.
    """
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')
    xs = data[0]
    ys = data[1]
    zs = data[2]
    ax.set_xlabel('lat')
    ax.set_ylabel('lon')
    ax.set_zlabel('height')
    a =[float(i)/max(count)*5 for i in count]
    print(a)
    for j in range(len(xs)):
        plt.plot(xs[j], ys[j], zs[j], linewidth=a[j], label="cluster " + str(j + 1) + "[" + str(count[j]) + "]")
    plt.tight_layout()
    plt.legend()
    return fig
