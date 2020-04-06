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


def vec_to_traj(vec, N):
    # Split vector containing N columns' worth of data into separate trajectories

    cutoffs = [0]
    interval_size = int(len(vec) / N)

    for n in range(N):
        n += 1
        cutoffs.append(n * interval_size)

    trajectories = []
    for c in range(len(cutoffs) - 1):
        trajectories.append(vec[cutoffs[c]:cutoffs[c + 1]])

    return trajectories
