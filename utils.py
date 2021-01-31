import json


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
