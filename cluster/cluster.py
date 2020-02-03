"""
Use various cluster algorithms to cluster trajectories
"""

import json
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import KMeans
from utils import vector
import reader.NovClim.reader as rd
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


def toVector(dimensionArray1, dimensionArray2, n=8756):
    data = []

    for i in range(n):
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

    N = max(labels) + 1

    for n in range(N):
        cluster = get_cluster(X, labels, n)
        cent = centroid(cluster)
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

# Function to handle request for kmeans clustering of a sector
def kmeans_request(dim1, dim2):
    model = KMeans

# WRITE FUNCTION TO HANDLE HIERARCHICAL LINKAGE MATRIX REQUEST




if __name__ == "__main__":
    time, lat, lon, height, pressure = rd.initialise(
        "../data/Trajectories/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")

    X = toVector(lat, lon)

    # store_linkage(X)

    Z = open_linkage()

    cc = fcluster(Z, 8, criterion='maxclust')

    print(cc)
    print(max(cc), min(cc))




