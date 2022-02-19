import json


def get_secret(key: str):
    return parse_json('res/secret.json', key)


def get_const(key: str):
    return parse_json('res/const.json', key)


def parse_json(path: str, key: str):
    """
    Parse json file and return value of key

    :param path: path to json file
    :param key: key to get value
    :return: value of key
    """
    with open(path, 'r') as file:
        const = json.load(file)

    key = key.split('.')
    while key:
        const = const[key.pop(0)]

    return const
