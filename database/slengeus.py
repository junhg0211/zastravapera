from database import Word


class SlengeusWord(Word):
    back_slice = 3

    def __init__(self, shape: str, code: str, word: str, noun='', verb='', adj='', adv='', note='', etymology='',
                 *args):
        super().__init__(word)

        self.shape = shape
        self.code = code
        self.noun = noun
        self.verb = verb
        self.adj = adj
        self.adv = adv
        self.note = note
        self.etymology = etymology

    def get_field_value(self) -> str:
        definitions = list()

        if self.noun:
            definitions.append(f'* **명** {self.noun}')
        if self.verb:
            definitions.append(f'* **동** {self.verb}')
        if self.adj:
            definitions.append(f'* **형** {self.adj}')
        if self.adv:
            definitions.append(f'* **부** {self.adv}')
        if self.note:
            definitions.append(f'* **비고** {self.note}')
        if self.etymology and self.etymology != '선험':
            definitions.append(f'* **어원** {self.etymology}')

        return '\n'.join(definitions)

    def get_field_name(self, special: bool) -> str:
        return f'__**{self.word} #{self.code}** (일치)__' if special else f'**{self.word} #{self.code}**'
