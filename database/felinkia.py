from database import Word


class FelinkiaWord(Word):
    back_slice = 1

    def __init__(self, word: str, noun: str, adjective: str, verb: str, adverb: str, conj: str, remark: str):
        super().__init__(word)
        self.noun = noun
        self.adjective = adjective
        self.verb = verb
        self.adverb = adverb
        self.conj = conj
        self.remark = remark

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
        if self.conj:
            definitions.append(f'접: {self.conj}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)
