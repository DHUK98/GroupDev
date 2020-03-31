# calculate average of certain field over list of trajectories
#

import json


def average(lst):
    return sum(lst) / len(lst)


def get_median_colours(trajs, labels, field):

    traj_avgs = []
    c_avgs_list_dict = {}
    c_avgs = {}
    hsl_vals = []

    # first average each trajectory
    for t in range(len(trajs[field])):
        traj_avgs.append(average(trajs[field][t]))

    # print(traj_avgs)

    for t in range(len(traj_avgs)):
        avg = traj_avgs[t]
        cluster_no = labels[t]

        if cluster_no in c_avgs_list_dict:
            c_avgs_list_dict[cluster_no].append(avg)
        else:
            c_avgs_list_dict[cluster_no] = [avg]

    # then finally iterate through the cluster numbers and average them out over the cluster
    for c_num, avgs in c_avgs_list_dict.items():
        c_avgs[c_num] = average(avgs)

    m = max(c_avgs.values())
    norm_avgs = [float(a) / m for a in c_avgs.values()]

    print(norm_avgs)

    # get hsl values for each one
    for n_avg in range(len(norm_avgs)):
        hsl_vals.append(avg_to_hsl(norm_avgs[n_avg]))

    return hsl_vals


# 1 - 100 is red-orange-yellow-green
def avg_to_hsl(n_avg):

    # for red - green-ish
    n_avg = n_avg * 100

    # hue, set saturation=100 and lightness=50 in CSS
    return n_avg

#
#
#
#
# if __name__ == "__main__":
#     with open("../static/stations/CGR/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.json", "r") as f:
#         trajs = json.load(f)
#
#
#     get_median_averages(trajs, [], "height")