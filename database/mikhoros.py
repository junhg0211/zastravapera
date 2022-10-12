from database import Word


class MikhorosWord(Word):
    def __init__(self, word: str, id_: str = '', noun: str = '', verb: str = '', etc: str = ''):
        super().__init__(word)
        self.id = id_
        self.noun = noun
        self.verb = verb
        self.etc = etc

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명. {self.noun}')
        if self.verb:
            definitions.append(f'동. {self.verb}')
        return '\n'.join(definitions)

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}** #{self.id}' if not special else f'__**{self.word}** #{self.id} (일치)__'
