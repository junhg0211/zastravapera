from database import Word


class SesameWord(Word):
    def __init__(self, word: str, pronunciation: str, origin: str, object_: str, action: str, property_: str, target: str,
                 *notes: str):
        super().__init__(word)
        self.pronunciation = pronunciation
        self.origin = origin
        self.object = object_
        self.action = action
        self.property = property_
        self.target = target
        self.notes = notes

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}[{self.pronunciation}]**' if not special \
            else f'__**{self.word}[{self.pronunciation}]** (일치)__'

    def get_field_value(self) -> str:
        definitions = list()
        if self.object:
            definitions.append(f'[객체] {self.object}')
        if self.action:
            definitions.append(f'[동작] {self.action}')
        if self.property:
            definitions.append(f'[속성] {self.property}')
        if self.target:
            definitions.append(f'[대상] {self.target}')
        return '\n'.join(definitions)
