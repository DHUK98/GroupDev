import os

import ujson as json


def list_files(path):
    output = []
    for file in os.listdir(path):
        if file.endswith(".json") and not file.startswith("info"):
            output.append(path + file)
    return output


def get_data(path, i):
    files = list_files(path)
    print(files[i])
    with open(files[i]) as json_file:
        data = json.load(json_file)
    print("loaded")
    return data


def get_datas(path, iis):
    files = list_files(path)
    data = []
    for i in iis:
        with open(files[i]) as json_file:
            print("loaded: " + files[i])
            data.append(json.load(json_file))
    acc = None
    for d in data:
        if not acc:
            acc = d
        else:
            print("merge")
            for k in acc.keys():
                acc[k].extend(d[k])

            print("merging done")
            print(len(acc["lat"]))
    return acc


def apply_mask(mask, d):
    for i, keep in enumerate(mask):
        if not keep:
            for key in d:
                del d[key][i - len(mask)]
    return d
