import os

import ujson as json
from copy import deepcopy
import ujson as json

def list_files(path, with_path=True):
    output = []
    for file in os.listdir(path):
        if file.endswith(".json") and not file.startswith("info") and not file.startswith("keys"):
            if with_path:
                output.append(os.path.join(path, file))
            else:
                output.append(file)
    output.sort()
    return output


def get_data(path, i):
    files = list_files(path)
    print(files[i])
    with open(files[i]) as json_file:
        data = json.load(json_file)
    print("loaded")
    return data


def get_keys(path):
    files = list_files(path, with_path=False)
    files = [os.path.join(path, ("keys_" + s)) for s in files]
    data = []
    for f in files:
        with open(f) as json_file:
            data.append(json.load(json_file))
    return data


def get_datas(path, iis):
    files = list_files(path)
    data = []
    for i in iis:
        with open(files[i]) as json_file:
            print("loaded: " + files[i])
            data.append(json.load(json_file))
    acc = None
    ommitted = set()
    for d in data:
        if not acc:
            acc = d
        else:
            print("merge")
            ommitted.update(set(set(acc.keys()).symmetric_difference(set(d.keys()))))

            rem = []
            for k in acc.keys():
                if k in d:
                    acc[k].extend(d[k])
                else:
                    rem.append(k)

            for r in rem:
                del acc[r]

            print("merging done")
            print(len(acc["lat"]))
    print(ommitted)
    print(acc.keys())
    return acc, list(acc.keys())


def apply_mask(mask, d):
    # do not remove json.load(json.dumps( it may look weird but its much faster than deepcopy
    data = json.loads(json.dumps(d))
    if not mask:
        return data
    for i, keep in enumerate(mask):
        if not keep:
            for key in data:
                del data[key][i - len(mask)]
    return data
