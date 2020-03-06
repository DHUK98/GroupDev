"""
Use various cluster algorithms to cluster trajectories
"""

import json
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import KMeans, SpectralClustering, DBSCAN
from . import vector
import pickle
import numpy as np
from collections import Counter

'''
General utility functions
'''


def get_trajectory_array(dimensionArray, n):
    # Return a 241 point array of the different data points for a particular dimension dimension should be a string of
    # either time, latitude, longitude, height, or pressure n is which trajectory - from 0 to 8756. Each one is a
    # different 241 point array for that particular aerosol particle's journey

    if n > 8756 or n < 0:
        print("Please use valid value for n")
        return
    else:
        return dimensionArray[n]


def toVector(dimensionArray1, dimensionArray2):
    data = []

    for i in range(len(dimensionArray1)):
        tempList1 = get_trajectory_array(dimensionArray1, i)
        tempList2 = get_trajectory_array(dimensionArray2, i)

        data.append(vector.trajToVec(tempList1, tempList2))

    X = np.array(data)

    return X


def get_cluster(data, data_labels, target_label):
    # Get all the data points in a cluster
    data_points = []
    for i in range(len(data_labels)):
        if data_labels[i] == target_label:
            data_points.append(data[i])
    return data_points


def store_linkage(X):
    # Store linkage matrix of passed data to be later used in clustering

    # Get linkage matrix
    Z = linkage(X, 'ward')

    file = open('linkage.txt', 'wb')
    pickle.dump(Z, file)
    file.close()


def open_linkage():
    # Open file containing most recently stored linkage matrix

    file = open('linkage.txt', 'rb')
    Z = pickle.load(file)

    return Z


def centroid(cluster):
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


def get_centroids(X, labels):
    # banter
    centroids = [[], []]

    N = max(labels)

    for n in range(N):
        n += 1  # Avoid off by 1 error, scipy labels clusters from 1-8 not 0-7

        cluster = get_cluster(X, labels, n)

        cent = centroid(cluster)

        lat, lon = vector.vecToTraj(cent)

        centroids[0].append(lat)
        centroids[1].append(lon)

    return centroids


# separate request function for dbscan
def cluster_request_dbscan(json_msg, min_samples=70, eps=50):

    # Take input of json message containing array of dimension 1, array of dimension 2 (generally lat and lon), and
    # number of clusters
    # Read json message
    loaded = json.loads(json_msg)

    dim1 = loaded.get('lat')
    dim2 = loaded.get('lon')

    X = toVector(dim1, dim2)

    model = DBSCAN(min_samples=min_samples, eps=eps).fit(X)
    labels = model.labels_

    # Convert to same labelling system as scipy: 1 -> N not 0 -> N-1
    for i in range(len(labels)):
        labels[i] += 1

    centroids = get_centroids(X, labels)

    json_dict = {'labels': labels.tolist(),
                 'centroids': centroids
                 }
    json_msg = json.dumps(json_dict)

    return json_msg


# Handle cluster requests except hierarchical
def cluster_request(json_msg, cluster_no, cluster_type, min_samples=70, eps=50):
    # Take input of json message containing array of dimension 1, array of dimension 2 (generally lat and lon), and
    # number of clusters

    # Read json message
    loaded = json.loads(json_msg)

    dim1 = loaded.get('lat')
    dim2 = loaded.get('lon')

    X = toVector(dim1, dim2)

    try:
        if cluster_type == 'kmeans':
            model = KMeans(n_clusters=int(cluster_no)).fit(X)
            # labels = model.labels_

        elif cluster_type == 'spectral':
            model = SpectralClustering(n_clusters=int(cluster_no)).fit(X)
            # labels = model.labels_

        elif cluster_type == 'dbscan':
            model = DBSCAN(min_samples=min_samples, eps=eps).fit(X)

        labels = model.labels_

        # Convert to same labelling system as scipy: 1 -> N not 0 -> N-1
        for i in range(len(labels)):
            labels[i] += 1

        centroids = get_centroids(X, labels)

        json_dict = {'labels': labels.tolist(),
                     'centroids': centroids
                     }
        json_msg = json.dumps(json_dict)

        return json_msg

    # Error handling for empty trajectory list
    except ValueError:
        print('No trajectories found in that sector/filter')

        json_dict = {'labels': [],
                     'centroids': []
                     }
        json_msg = json.dumps(json_dict)

        return json_msg


# Eliminate noisy trajectories using DBSCAN then
def dbscan_kmeans(json_msg, cluster_no, min_samples, eps):
    # Take input of json message containing array of dimension 1, array of dimension 2 (generally lat and lon), and
    # number of clusters
    # Read json message
    loaded = json.loads(json_msg)

    dim1 = loaded.get('lat')
    dim2 = loaded.get('lon')

    X = toVector(dim1, dim2)

    model_dbscan = DBSCAN(min_samples=min_samples, eps=eps).fit(X)

    # Filter out trajectories that were judged as noise by DBSCAN
    X_noise_free = []
    noisy = []

    for i in range(len(X)):
        if model_dbscan.labels_[i] != -1:
            X_noise_free.append(X[i])
        else:
            noisy.append(X[i])

    print(len(noisy))

    model_kmeans = KMeans(n_clusters=int(cluster_no)).fit(X_noise_free)

    centroids_kmeans = get_centroids(X, model_kmeans.labels_)

    json_dict = {'labels': model_kmeans.labels_.tolist(),
                 'centroids': centroids_kmeans
                 }

    json_msg = json.dumps(json_dict)

    return json_msg

# Function to handle request for kmeans clustering of a sector
def kmeans_request(json_msg, cluster_no):
    # Take input of json message containing array of dimension 1, array of dimension 2 (generally lat and lon), and
    # number of clusters

    # Read json message
    loaded = json.loads(json_msg)

    dim1 = loaded.get('lat')
    dim2 = loaded.get('lon')

    X = toVector(dim1, dim2)

    model = KMeans(n_clusters=int(cluster_no)).fit(X)

    labels = model.labels_

    # Convert to same labelling system as scipy: 1 -> N not 0 -> N-1
    for i in range(len(labels)):
        labels[i] += 1

    centroids = get_centroids(X, labels)

    json_dict = {'labels': labels.tolist(),
                 'centroids': centroids
                 }
    json_msg = json.dumps(json_dict)

    return json_msg


def linkage_request(json_data):
    # Take input of json message containing nested array containing data for dimension 1,
    # nested array containing data for dimension 2 (usually lat and lon)

    # Read json message
    loaded = json.loads(json_data)
    # Turn to cluster-able vector
    X = toVector(loaded.get('lat'), loaded.get('lon'))

    # Get linkage matrix
    Z = linkage(X, 'ward')

    json_dict = {'Z': Z.tolist()}

    json_msg = json.dumps(json_dict)

    return json_msg


def h_cluster_request(json_data, json_Z, cluster_no):
    # Take input of json message containing linkage matrix Z and no. of clusters

    # Read json message
    loaded_data = json.loads(json_data)

    Z = json.loads(json_Z).get('Z')
    X = toVector(loaded_data.get('lat'), loaded_data.get('lon'))

    labels = fcluster(Z, cluster_no, criterion='maxclust')

    centroids = get_centroids(X, labels)

    json_dict = {'labels': labels.tolist(),
                 'centroids': centroids
                 }
    json_msg = json.dumps(json_dict)

    return json_msg
