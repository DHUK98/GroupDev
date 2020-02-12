''''
Module for converting data to/from vectors
'''

import numpy as np


def trajToVec(dim1, dim2):
    # Convert 2 trajectory dimensions into a vector (numpy array) of dimensions equal to sum of total data
    # E.g. [0,1,2] and [3,4,5] -> array [0,1,2,3,4,5]

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
    # Convert vector (numpy array) into 2 trajectory dimensions
    # E.g. array [0,1,2,3,4,5] -> [0,1,2] and [3,4,5]


    dim1 = vec[:len(vec) // 2]
    dim2 = vec[len(vec) // 2:]

    return dim1, dim2