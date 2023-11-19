from database import Word, PosDatabase


class RoponaWord(Word):
    back_slice = 3

    def __init__(self, word: str, pronunciation_modern: str, pronunciation_middle: str, pronunciation_old: str,
                 pronunciation_hyper: str, pos: str, meaning: str, accent: str, traditional: str):
        super().__init__(word)
        self.word = word
        self.pronunciation_modern = pronunciation_modern
        self.pronunciation_middle = pronunciation_middle
        self.pronunciation_old = pronunciation_old
        self.pronunciation_hyper = pronunciation_hyper
        self.pos = pos
        self.meaning = meaning
        self.accent = accent
        self.traditional = traditional

    def get_field_name(self, special: bool) -> str:
        if special:
            return f'__**{self.word} [{self.pronunciation_modern}]** ({self.pos})__'
        else:
            return f'**{self.word} [{self.pronunciation_modern}]** ({self.pos})'

    def get_field_value(self) -> str:
        return (f'({self.accent}) ' if self.accent else '') + f'{self.meaning}'


class RoponaDatabase(PosDatabase):
    def __init__(self, spreadsheet_key: str):
        super().__init__(spreadsheet_key, 1, 0, 5, 6)

        self.pronunciation_modern_column = 1
        self.pronunciation_middle_column = 2
        self.pronunciation_old_column = 3
        self.pronunciation_hyper_column = 4
        self.accent_column = 7
        self.traditional_column = 8

    def row_appending(self, rows_list, row):
        rows_list.append(RoponaWord(
            row[self.word_column], row[self.pronunciation_modern_column], row[self.pronunciation_middle_column],
            row[self.pronunciation_old_column], row[self.pronunciation_hyper_column], row[self.pos_column],
            row[self.meaning_column], row[self.accent_column], row[self.traditional_column]))