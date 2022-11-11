from database import Word


class FsovmWord(Word):
    back_slice = 1

    def __init__(self, word: str, noun: str, adjective: str, verb: str, adverb: str, postpos: str, int):
        super().__init__(word)
        self.noun = noun
        self.adjective = adjective
        self.verb = verb
        self.adverb = adverb
        self.postpos = postpos
        self.int = int

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
        if self.int:
            definitions.append(f'감 {self.int}')
        return '\n'.join(definitions)