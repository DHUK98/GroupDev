"""
Use various cluster algorithms to cluster trajectories
"""

import reader.NovClim.reader as rd
from utils import vector
from cluster import cluster_utils

import numpy as np
from matplotlib import pyplot as plt

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import davies_bouldin_score

import json
from scipy.cluster.hierarchy import dendrogram, linkage


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
        cluster = cluster_utils.get_cluster(data, labels, n)
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

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


if __name__ == "__main__":
    time, lat, lon, height, pressure = rd.initialise(
        "../data/Trajectories/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")

    x = cluster_utils.toVector(lat, lon)

    X = x[:100]

    n = 4
    # cluster_model = KMeans(n_clusters=n)
    cluster_model = AgglomerativeClustering(n_clusters=None, distance_threshold=0)
    cluster_model.fit(X)

    centroids = all_centroids(X, cluster_model.labels_)


    # for c in centroids:
    #     y = [i for i in range(len(c))]
    #     plt.scatter(c[0], c[1])
    #     plt.show()

    # plot the top three levels of the dendrogram
    plot_dendrogram(cluster_model, truncate_mode='level', p=3)

    j = buildJson(centroids)
    print('done')
    # print(j)
