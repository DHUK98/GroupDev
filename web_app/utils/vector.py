''''
Module for converting data between individual trajectory columns and vectors that can be used in clustering
'''

import numpy as np

def traj_to_vec(dims):
#     Convert list of trajectory columns (usually 2 or 3) into single vector

    vec = []

    for d in range(len(dims)):
        for item in dims[d]:
            vec.append(item)

    return vec

# OLD VERSION
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

def vec_to_traj(vec, N):
    # Split vector containing N columns' worth of data into separate trajectories

    cutoffs = [0]
    interval_size = int(len(vec)/N)

    for n in range(N):
        n+=1
        cutoffs.append(n*interval_size)

    trajectories = []
    for c in range(len(cutoffs)-1):
        trajectories.append(vec[cutoffs[c]:cutoffs[c+1]])

    return trajectories

# OLD VERSION
def vecToTraj(vec):
    # Convert vector (numpy array) into 2 trajectory dimensions
    # E.g. array [0,1,2,3,4,5] -> [0,1,2] and [3,4,5]


    dim1 = vec[:len(vec) // 2]
    dim2 = vec[len(vec) // 2:]

    return dim1, dim2

