from database import Word


class MikhorosWord(Word):
    def __init__(self, word: str, number: str = '', noun: str = '', verb: str = ''):
        super().__init__(word)
        self.number = number
        self.noun = noun
        self.verb = verb

    # noinspection DuplicatedCode
    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명. {self.noun}')
        if self.verb:
            definitions.append(f'동. {self.noun}')
        return '\n'.join(definitions)

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}** #{self.number}' if not special else f'__**{self.word}** #{self.number} (일치)__'



