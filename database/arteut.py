from database import Word


class ArteutWord(Word):
    def __init__(self, word: str, number: str = '', noun: str = '', det: str = '', adj: str = '', rel: str = '',
                 verb: str = '', exp: str = '', note: str = '', source: str = '', origin: str = '', maker: str = ''):
        super().__init__(word)
        self.number = number
        self.noun = noun
        self.det = det
        self.adj = adj
        self.rel = rel
        self.verb = verb
        self.exp = exp
        self.note = note
        self.source = source
        self.origin = origin
        self.maker = maker

    # noinspection DuplicatedCode
    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명. {self.noun}')
        if self.det:
            definitions.append(f'한. {self.noun}')
        if self.adj:
            definitions.append(f'형. {self.noun}')
        if self.rel:
            definitions.append(f'관. {self.noun}')
        if self.verb:
            definitions.append(f'동. {self.noun}')
        if self.exp:
            definitions.append(f'감. {self.noun}')
        if self.note:
            definitions.append(f'비고. {self.noun}')
        return '\n'.join(definitions)

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}** #{self.number}' if not special else f'__**{self.word}** #{self.number} (일치)__'
