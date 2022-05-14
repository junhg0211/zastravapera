from util.general import normalise


def zasokese_to_simetasise(sentence: str) -> str:
    """ 자소크어 문자열을 시메타시스어 문자열로 변환합니다. """

    result = ''
    words = sentence.split(' ')
    for word in words:
        punctuation = ''
        while word[-1] in '.,;:?!\"\']':
            punctuation = word[-1] + punctuation
            word = word[:-1]

        word = word.replace('y', 'ú').replace('j', 'y').replace('ÿ', 'yú')
        word = word.replace('c', 'ch')
        if word.endswith('que'):
            word = word[:-3] + 'c'
        if word.endswith('iê'):
            word = word[:-1] + 'ee'
        if word.endswith('g'):
            word = word[:-1] + 'c'
        if word.endswith('d'):
            word = word[:-1] + 't'
        if word.endswith('v'):
            word = word[:-1] + 'p'
        if word.endswith('s'):
            word = word[:-1] + 'ch'
        word = word\
            .replace('ä', 'ae') \
            .replace('ë', 'ee') \
            .replace('ï', 'ie') \
            .replace('ö', 'oe') \
            .replace('ü', 'ue')
        word = normalise(word)
        word = word\
            .replace('qua', 'ca') \
            .replace('que', 'ke') \
            .replace('qui', 'ki') \
            .replace('quo', 'co')
        word = word.replace('sh', 'z')
        word = word.replace('v', 'b')

        word += punctuation
        result += word + ' '
    return result.rstrip()
