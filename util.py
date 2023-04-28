import json


def load_config():
    fd = open("./config.json")
    data = json.loads(fd.read())
    return data
