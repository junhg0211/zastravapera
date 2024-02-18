from database import Word


class PaselWord(Word):
    back_slice = 2

    def __init__(self, code: str = '', word: str = '', noun: str = '', verb: str = '', adj: str = '', etc: str = '',
                 note: str = '', derived_from_language: str = '', derived_from_word: str = ''):
        super().__init__(word)
        self.code = code
        self.noun = noun
        self.verb = verb
        self.adj = adj
        self.etc = etc
        self.note = note
        self.derived_from_language = derived_from_language
        self.derived_from_word = derived_from_word

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}**#{self.code}' if not special else f'__**{self.word}**#{self.code} (일치)__'

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'* {self.noun}')
        if self.verb:
            definitions.append(f'* {self.verb}')
        if self.adj:
            definitions.append(f'* {self.adj}')
        if self.etc:
            definitions.append(f'* {self.etc}')
        if self.note:
            definitions.append(f'* {self.note}')
        return '\n'.join(definitions)
