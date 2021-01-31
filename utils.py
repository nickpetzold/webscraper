import json


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(data, path, file_type):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"{file_type} printed to {path}")
