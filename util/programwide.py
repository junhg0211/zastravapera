variables = dict()


def set_programwide(key, value):
    variables[key] = value
    return value


def get_programwide(key):
    return variables[key]