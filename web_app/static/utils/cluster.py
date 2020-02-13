"""
Use various cluster algorithms to cluster trajectories
"""

import json
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import KMeans
from . import vector
import pickle
import numpy as np

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
    # Get all centroids from the clustering
    centroids = []

    N = max(labels)

    for n in range(N):
        n += 1  # Avoid off by 1 error, scipy labels clusters from 1-8 not 0-7
        cluster = get_cluster(X, labels, n)
        cent = centroid(cluster)
        dim1, dim2 = vector.vecToTraj(cent)

        centroids.append((tuple(dim1), tuple(dim2)))

    return centroids


# # Build a JSON message containing the cluster centroids
# def centroids_json(centroids):
#     centroid_dic = {}
#
#     for c in range(len(centroids)):
#         # key = "cluster " + str(c)
#
#         centroid_dic.update({c: centroids[c]})
#
#     json_msg = json.dumps(centroid_dic)
#
#     return json_msg

# Function to handle request for kmeans clustering of a sector
def kmeans_request(json_msg):
    # Take input of json message containing array of dimension 1, array of dimension 2 (generally lat and lon), and
    # number of clusters

    # Read json message
    loaded = json.loads(json_msg)

    dim1 = loaded.get('dim1')
    dim2 = loaded.get('dim2')
    cluster_no = loaded.get('cluster_no')

    X = toVector(dim1, dim2)

    model = KMeans(n_clusters=cluster_no).fit(X)

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


# WRITE FUNCTION TO HANDLE HIERARCHICAL LINKAGE MATRIX REQUEST
def linkage_request(json_msg):
    # Take input of json message containing array of dimension 1, array of dimension 2 (generally lat and lon)

    # Read json message
    loaded = json.loads(json_msg)
    # Turn to cluster-able vector
    X = toVector(loaded.get('lat'), loaded.get('lon'))

    # Get linkage matrix
    Z = linkage(X, 'ward')

    json_dict = {'Z': Z.tolist()}

    json_msg = json.dumps(json_dict)

    return json_msg


def h_cluster_request(json_msg):
    # Take input of json message containing linkage matrix Z and no. of clusters

    # Read json message
    loaded = json.loads(json_msg)

    Z = loaded.get('Z')
    cluster_no = loaded.get('cluster_no')
    X = toVector(loaded.get('dim1'), loaded.get('dim2'))

    labels = fcluster(Z, cluster_no, criterion='maxclust')

    centroids = get_centroids(X, labels)

    json_dict = {'labels': labels.tolist(),
                 'centroids': centroids
                 }
    json_msg = json.dumps(json_dict)

    return json_msg
