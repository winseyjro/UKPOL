import json


def write_json(filepath, data, mode='w'):
    with open(filepath, mode, encoding='utf-8') as outfile:
        json.dump(data, outfile)


def read_json(filepath, mode='r'):
    with open(filepath, mode, encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data
