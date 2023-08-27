from database import Word


class LazhonWord(Word):
    def __init__(self, word: str, noun: str, verb: str, adjective: str, adverb: str, postpos: str, conjuction: str, others: str, note: str, yuynyny: str, yuyn: str):
        super().__init__(word)
        self.noun = noun
        self.verb = verb
        self.adjective = adjective
        self.adverb = adverb
        self.postpos = postpos
        self.conjuction = conjuction
        self.others = others
        self.note = note

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명: {self.noun}')
        if self.verb:
            definitions.append(f'동: {self.verb}')
        if self.adjective:
            definitions.append(f'형용: {self.adjective}')
        if self.adverb:
            definitions.append(f'부: {self.adverb}')
        if self.postpos:
            definitions.append(f'조: {self.postpos}')
        if self.conjuction:
            definitions.append(f'접속: {self.conjuction}')
        if self.others:
            definitions.append(f'기타: {self.others}')
        if self.note:
            definitions.append(f'비고: {self.note}')
        return '\n'.join(definitions)
