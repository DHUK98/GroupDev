from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import numpy as np
from cluster import cluster_utils
import reader.NovClim.reader as rd
import pickle


def store_linkage(X):
    #Store linkage matrix of passed data to be later used in clustering

    #Get linkage matrix
    Z = linkage(X, 'ward')

    file = open('linkage.txt', 'wb')
    pickle.dump(Z, file)
    file.close()

def open_linkage():
    #Open file containing most recently stored linkage matrix

    file = open('linkage.txt', 'rb')
    Z = pickle.load(file)

    return Z


if __name__ == "__main__":

    time, lat, lon, height, pressure = rd.initialise(
            "../data/Trajectories/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")

    X = cluster_utils.toVector(lat, lon)

    store_linkage(X)

    Z = open_linkage()

    k = 4
    clusters = fcluster(Z, k, criterion='maxclust')

    for i in clusters:
        print(i)


