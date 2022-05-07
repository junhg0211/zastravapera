variables = dict()


def set_programwide(key, value):
    """ 프로그램 전반적인 Global 변수를 불러옵니다. """
    variables[key] = value
    return value


def get_programwide(key):
    """ 프로그램 전반적인 Global 변수를 설정합니다. """
    return variables[key]
