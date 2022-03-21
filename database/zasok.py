from discord import Embed

from database import Word


class ZasokeseWord(Word):
    back_slice = 2

    def __init__(self, word: str, noun: str = '', adj: str = '', verb: str = '', adv: str = '', prep: str = '',
                 conj: str = '', remark: str = '', derived_from_language: str = '', derived_from_word: str = ''):
        super().__init__(word)
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.prep = prep
        self.conj = conj
        self.remark = remark
        self.derived_from_language = derived_from_language
        self.derived_from_word = derived_from_word

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
        if self.conj:
            definitions.append(f'접: {self.conj}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


class BerquamWord(Word):
    def __init__(self, word: str, noun: str = '', adj: str = '', verb: str = '', adv: str = '', remark: str = ''):
        super().__init__()
        self.word = word
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.remark = remark

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_value = self.get_field_value()
        embed.add_field(
            name=f'**{self.word}**' if not special else f'__**{self.word}** (일치)__',
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

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