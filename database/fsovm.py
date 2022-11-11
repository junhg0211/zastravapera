from database import Word


class FsovmWord(Word):
    def __init__(self, word: str, noun: str, adjective: str, verb: str, adverb: str, postpos: str, interj):
        super().init(word)
        self.noun = noun
        self.adjective = adjective
        self.verb = verb
        self.adverb = adverb
        self.postpos = postpos
        self.interj = interj

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명: {self.noun}')
        if self.adjective:
            definitions.append(f'형: {self.adjective}')
        if self.verb:
            definitions.append(f'동: {self.verb}')
        if self.adverb:
            definitions.append(f'부: {self.adverb}')
        if self.postpos:
            definitions.append(f'조 {self.postpos}')
        if self.interj:
            definitions.append(f'감 {self.interj}')
        return '\n'.join(definitions)