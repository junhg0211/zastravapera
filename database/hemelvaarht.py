from discord import Embed

from database import Word


class ThravelemehWord(Word):
    back_slice = 2

    def __init__(self, word: str, noun: str = '', verb: str = '', adj: str = '', adv: str = '', conj: str = '',
                 remark: str = '', cont: str = '', origin_language: str = '', origin: str = ''):
        super().__init__(word)
        self.noun = noun
        self.verb = verb
        self.adj = adj
        self.adv = adv
        self.conj = conj
        self.remark = remark
        self.cont = cont
        self.origin_language = origin_language
        self.origin = origin

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_value = self.get_field_value()
        embed.add_field(
            name=f'[{self.cont}] **{self.word}**' if not special else f'__[{self.cont}] **{self.word}** (일치)__',
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'[명] {self.noun}')
        if self.verb:
            definitions.append(f'[동] {self.verb}')
        if self.adj:
            definitions.append(f'[형] {self.adj}')
        if self.adv:
            definitions.append(f'[부] {self.adv}')
        if self.conj:
            definitions.append(f'[접] {self.conj}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


