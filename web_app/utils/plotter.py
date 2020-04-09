import matplotlib.pyplot as plt
from flask import session
import ujson as json


def plot_svg(data, keys, count):
    """ renders the plot on the fly.
    """
    fig = plt.figure(figsize=(4, 4))
    xs = []
    ys = []

    if len(data) == 1:
        ys = data[0]
        xs = list(range(240, -1, -1))
        plt.xlabel("time")
        plt.ylabel(keys[0])
    else:
        xs = data[0]
        ys = data[1]
        plt.xlabel(keys[0])
        plt.ylabel(keys[1])

    a = [float(i) / max(count) * 5 for i in count]
    print(a)
    print(count)
    for j in range(len(xs)):
        plt.plot(xs[j], ys[j], linewidth=a[j], label="cluster " + str(j + 1) + "[" + str(count[j]) + "]")
    plt.tight_layout()
    plt.legend()
    plt.close()
    return fig


def plot_svg3d(data, keys, count):
    """ renders the plot on the fly.
    """
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel(keys[0])
    ax.set_ylabel(keys[1])
    ax.set_zlabel(keys[2])
    a = [float(i) / max(count) * 5 for i in count]

    xs = data[0]
    ys = data[1]
    zs = data[2]

    for j in range(len(xs)):
        plt.plot(xs[j], ys[j], zs[j], linewidth=a[j], label="cluster " + str(j + 1) + "[" + str(count[j]) + "]")
    plt.tight_layout()
    plt.legend()
    plt.close()
    return fig
