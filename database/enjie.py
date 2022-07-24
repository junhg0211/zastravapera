from database import PosDatabase, PosWord


class EnjieWord(PosWord):
    def __init__(self, word: str, pos: str, meaning: str, reading: str, animate: str, vowel: str, accent: str):
        super().__init__(word, pos, meaning)
        self.reading = reading
        self.animate = animate
        self.vowel = vowel
        self.accent = accent

    def get_field_name(self, special: bool) -> str:
        return (f'**{self.word} ({self.reading})**' if not special else f'__**{self.word} ({self.reading})** (일치)__') \
               + (f' [{self.note}]' if self.note else '')

    def get_field_value(self) -> str:
        parts = list()
        if self.animate:
            parts.append(self.animate)
        if self.vowel:
            parts.append(self.vowel)
        if self.pos:
            parts.append(self.pos)

        return f'[' + f' '.join(parts) + ']' + (f'({self.accent})' if self.accent else '') + f'{self.meaning}'


class EnjieDatabase(PosDatabase):
    def __init__(self, spreadsheet_key: str):
        super().__init__(spreadsheet_key, 1, 1, 3, 2)
        self.reading_column = 0
        self.animate_noun = 4
        self.vowel_type = 5
        self.accent = 6

    def row_appending(self, rows_list, row):
        rows_list.append(EnjieWord(
            row[self.word_column], row[self.pos_column], row[self.meaning_column], row[self.reading_column],
            row[self.animate_noun], row[self.vowel_type], row[self.accent]))
