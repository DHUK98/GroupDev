'''
General utility functions applicable to all clustering approaches
'''

import numpy as np
from utils import vector


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