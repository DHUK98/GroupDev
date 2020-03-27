import os

import ujson as json


def list_files(path):
    output = []
    for file in os.listdir(path):
        if file.endswith(".json") and not file.startswith("info"):
            output.append(path + file)
    return output


def get_data(path,i):
    files = list_files(path)
    print(files[i])
    with open(files[i]) as json_file:
        data = json.load(json_file)
    print("loaded")
    return data


def apply_mask(mask, d):
    for i, keep in enumerate(mask):
        if not keep:
            for key in d:
                del d[key][i - len(mask)]
    return d
