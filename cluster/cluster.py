"""
Use various cluster algorithms to cluster trajectories
"""

import reader.NovClim.reader as rd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import davies_bouldin_score
import json
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt



# X = np.array([[5,3],
#     [10,15],
#     [15,12],
#     [24,10],
#     [30,30],
#     [85,70],
#     [71,80],
#     [60,78],
#     [70,55],
#     [80,91],])
#
# labels = range(1, 11)
# plt.figure(figsize=(10, 7))
# plt.subplots_adjust(bottom=0.1)
# plt.scatter(X[:,0],X[:,1], label='True Position')
#
# for label, x, y in zip(labels, X[:, 0], X[:, 1]):
#     plt.annotate(
#         label,
#         xy=(x, y), xytext=(-3, 3),
#         textcoords='offset points', ha='right', va='bottom')
# plt.show()
#
# linked = linkage(X, 'single')
#
# labelList = range(1, 11)
#
# plt.figure(figsize=(10, 7))
# dendrogram(linked,
#             orientation='top',
#             labels=labelList,
#             distance_sort='descending',
#             show_leaf_counts=True)
# plt.show()

def get_trajectory_array(dimensionArray, n):
    # Return a 241 point array of the different data points for a particular dimension dimension should be a string of
    # either time, latitude, longitude, height, or pressure n is which trajectory - from 0 to 8756. Each one is a
    # different 241 point array for that particular aerosol particle's journey

    if n > 8756 or n < 0:
        print("Please use valid value for n")
        return
    else:
        return dimensionArray[n]


def getData(dimensionArray1, dimensionArray2, n=8756):
    data = []

    for i in range(n):
        tempList1 = get_trajectory_array(dimensionArray1, i)
        tempList2 = get_trajectory_array(dimensionArray2, i)

        data.append(trajToVec(tempList1, tempList2))

    X = np.array(data)

    return X


def trajToVec(dim1, dim2):
    # Convert 2 dimensions into a vector of dimensions equal to sum of total data

    if len(dim1) != len(dim2):
        print("Dimensions do not match up")
    else:
        Xlist = []
        for item in dim1:
            Xlist.append(item)
        for item in dim2:
            Xlist.append(item)

        # print(len(Xlist))

        Xarray = np.array(Xlist)

        return Xarray


def vecToTraj(vec):
    list = vec

    dim1 = list[:len(list) // 2]
    dim2 = list[len(list) // 2:]

    return dim1, dim2


def test_scores(X):
    Xs = []
    Ys = []

    for n in range(20):
        m = (n * 30) + 310

        kmeans = KMeans(n_clusters=m)
        kmeans.fit(X)

        Xs.append(m)
        Ys.append(davies_bouldin_score(X, kmeans.labels_))

    return Xs, Ys


# Get all the data points in a cluster
def get_cluster(data, labels, label):
    data_points = []

    for i in range(len(labels)):
        if labels[i] == label:
            data_points.append(data[i])

    return data_points


# Get the mean trajectory in a cluster
def agg_centroid(cluster):
    vec_size = len(cluster[0])

    mean_vec = [0 for _ in range(vec_size)]

    for vector in cluster:
        for i in range(vec_size):
            mean_vec[i] += vector[i]

    for i in range(vec_size):
        mean_vec[i] /= len(cluster)

    return mean_vec


# Get all centroids from the clustering
def all_centroids(data, labels):
    centroids = []

    N = max(labels) + 1

    for n in range(N):
        cluster = get_cluster(data, labels, n)
        centroid = agg_centroid(cluster)
        dim1, dim2 = vecToTraj(centroid)

        centroids.append((tuple(dim1), tuple(dim2)))

    return centroids


# Build a JSON message containing the cluster centroids
def buildJson(centroids):
    centroid_dic = {}

    for c in range(len(centroids)):
        # key = "cluster " + str(c)

        centroid_dic.update({c: centroids[c]})

    json_msg = json.dumps(centroid_dic)

    return json_msg


if __name__ == "__main__":
    time, lat, lon, height, pressure = rd.initialise(
        "../Data/NovClim/Trajectories/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")

    X = getData(lat, lon)

    n = 4
    # cluster_model = KMeans(n_clusters=n)
    cluster_model = AgglomerativeClustering(n_clusters=n)
    cluster_model.fit(X)

    centroids = all_centroids(X, cluster_model.labels_)

    j = buildJson(centroids)
    print('done')
    # print(j)

