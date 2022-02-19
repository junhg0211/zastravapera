import unicodedata


def normalise(string: str):
    """
    Removes all the diacritic in the string and return it.

    :param string:
    :return:
    """

    return ''.join(c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn').lower()
