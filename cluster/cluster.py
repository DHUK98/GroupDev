"""
Use various cluster algorithms to cluster trajectories
"""

import reader.NovClim.reader as rd
import numpy as np
from utils import vector
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import davies_bouldin_score
import json
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt



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

        data.append(vector.trajToVec(tempList1, tempList2))

    X = np.array(data)

    return X


# def test_scores(X):
#     Xs = []
#     Ys = []
#
#     for n in range(20):
#         m = (n * 30) + 310
#
#         kmeans = KMeans(n_clusters=m)
#         kmeans.fit(X)
#
#         Xs.append(m)
#         Ys.append(davies_bouldin_score(X, kmeans.labels_))
#
#     return Xs, Ys


def get_cluster(data, labels, label):
    # Get all the data points in a cluster
    data_points = []

    for i in range(len(labels)):
        if labels[i] == label:
            data_points.append(data[i])

    return data_points


def agg_centroid(cluster):
    # Get the mean trajectory in a cluster
    vec_size = len(cluster[0])

    mean_vec = [0 for _ in range(vec_size)]

    for vector in cluster:
        for i in range(vec_size):
            mean_vec[i] += vector[i]

    for i in range(vec_size):
        mean_vec[i] /= len(cluster)

    return mean_vec



def all_centroids(data, labels):
    # Get all centroids from the clustering
    centroids = []

    N = max(labels) + 1

    for n in range(N):
        cluster = get_cluster(data, labels, n)
        centroid = agg_centroid(cluster)
        dim1, dim2 = vector.vecToTraj(centroid)

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
        "../data/Trajectories/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")

    X = getData(lat, lon)

    n = 4
    # cluster_model = KMeans(n_clusters=n)
    cluster_model = AgglomerativeClustering(n_clusters=n)
    cluster_model.fit(X)

    centroids = all_centroids(X, cluster_model.labels_)

    j = buildJson(centroids)
    print('done')
    print(j)
