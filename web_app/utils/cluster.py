"""
Use various cluster algorithms to cluster trajectories
"""

import json
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import KMeans, DBSCAN, MiniBatchKMeans
from . import vector
import pickle
import numpy as np

'''
Functions for all clustering of data
'''


def get_trajectory_array(dimensionArray, n):
    # Return a 241 point array of the different data points for a particular dimension dimension should be a string of
    # either time, latitude, longitude, height, or pressure n is which trajectory - from 0 to 8756. Each one is a
    # different 241 point array for that particular aerosol particle's journey
    return dimensionArray[n]


def get_cluster_points(data, data_labels, target_label):
    # Get all the data points in a cluster
    data_points = []
    for i in range(len(data_labels)):
        if data_labels[i] == target_label:
            data_points.append(data[i])
    return data_points


# def store_linkage(X):
#     # Store linkage matrix of passed data to be later used in clustering
#
#     # Get linkage matrix
#     Z = linkage(X, 'ward')
#
#     file = open('linkage.txt', 'wb')
#     pickle.dump(Z, file)
#     file.close()
#
#
# def open_linkage():
#     # Open file containing most recently stored linkage matrix
#
#     file = open('linkage.txt', 'rb')
#     Z = pickle.load(file)
#
#     return Z


def calculate_centroid(cluster):
    # Function to calculate the centroid (mean) of a cluster

    # Check for empty cluster
    if len(cluster[0]) == 0:
        return []
    # Get the mean trajectory in a cluster
    vec_size = len(cluster[0])

    mean_vec = [0 for _ in range(vec_size)]

    for vector in cluster:
        for i in range(vec_size):
            mean_vec[i] += vector[i]

    for i in range(vec_size):
        mean_vec[i] /= len(cluster)

    return mean_vec


def get_centroids(X, labels, N):
    # Find centroids of all clustered data
    #
    # X: List containing data in vector form
    # labels: List of cluster assignments
    centroids = [[] for _ in range(N)]

    cluster_no = max(labels)

    for c in range(cluster_no):
        c += 1  # Avoid off by 1 error, scipy labels clusters from 1-8 not 0-7

        cluster = get_cluster_points(X, labels, c)

        cent = calculate_centroid(cluster)

        dimensions = vector.vec_to_traj(cent, N)

        for n in range(N):
            centroids[n].append(dimensions[n])

    return centroids


# Function to handle both Kmeans and DBSCAN clustering, with potential to expand
def cluster_request(json_msg, keys, cluster_type, cluster_no=5, min_samples=70, eps=50):
    # Take input of json message containing array of dimension 1, array of dimension 2 (generally lat and lon), and
    # number of clusters

    print("Cluster type is " + str(cluster_type))

    # Read json message
    loaded = json.loads(json_msg)

    dimensions = []

    for k in keys:
        dimensions.append(loaded.get(k))

    X = vector.traj_to_vec(dimensions)

    try:
        if cluster_type == 'kmeans':
            model = KMeans(n_clusters=int(cluster_no)).fit(X)
            # model = MiniBatchKMeans(n_clusters=int(cluster_no), random_state=0, batch_size=10).fit(X)
            # labels = model.labels_

        elif cluster_type == 'dbscan':
            model = DBSCAN(min_samples=min_samples, eps=eps).fit(X)

        elif cluster_type == 'dbscan_kmeans':
            model_dbscan = DBSCAN(min_samples=min_samples, eps=eps).fit(X)

            # Filter out trajectories that were judged as noise by DBSCAN
            X_noise_free = []
            noisy = []

            for i in range(len(X)):
                if model_dbscan.labels_[i] != -1:
                    X_noise_free.append(X[i])
                else:
                    noisy.append(X[i])

            # Cluster remaining data using kmeans
            model = KMeans(n_clusters=int(cluster_no)).fit(X_noise_free)

        labels = model.labels_

        # Convert to same labelling system as scipy: 1 -> N not 0 -> N-1
        for i in range(len(labels)):
            labels[i] += 1

        centroids = get_centroids(X, labels)

        json_dict = {'labels': labels.tolist(),
                     'centroids': centroids,
                     'keys': keys
                     }
        json_msg = json.dumps(json_dict)

        return json_msg

    # Error handling for empty trajectory list
    except ValueError:
        print('No trajectories found in that sector/filter')

        json_dict = {'labels': [],
                     'centroids': [],
                     'keys': keys
                     }
        json_msg = json.dumps(json_dict)

        return json_msg

