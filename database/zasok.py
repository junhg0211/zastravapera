from database import Word


class ZasokeseWord(Word):
    back_slice = 2

    def __init__(self, code: str = '', word: str = '', noun: str = '', adj: str = '', verb: str = '', adv: str = '',
                 prep: str = '', remark: str = '', derived_from_language: str = '', derived_from_word: str = ''):
        super().__init__(word)
        self.code = code
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.prep = prep
        self.remark = remark
        self.derived_from_language = derived_from_language
        self.derived_from_word = derived_from_word

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}**#{self.code}' if not special else f'__**{self.word}**#{self.code} (일치)__'

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명: {self.noun}')
        if self.adj:
            definitions.append(f'형: {self.adj}')
        if self.verb:
            definitions.append(f'동: {self.verb}')
        if self.adv:
            definitions.append(f'부: {self.adv}')
        if self.prep:
            definitions.append(f'관: {self.prep}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


class BerquamWord(Word):
    def __init__(self, word: str, noun: str = '', adj: str = '', verb: str = '', adv: str = '', remark: str = ''):
        super().__init__(word)
        self.word = word
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.remark = remark

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명: {self.noun}')
        if self.adj:
            definitions.append(f'형: {self.adj}')
        if self.verb:
            definitions.append(f'동: {self.verb}')
        if self.adv:
            definitions.append(f'부: {self.adv}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)
