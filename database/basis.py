import re
from datetime import datetime, timedelta
from typing import Type, Tuple, List, Callable

import gspread
from discord import Embed

from const import get_const
from util.general import normalise


class Word:
    back_slice = 0
    leading_rows = 1

    def __init__(self, word: str):
        self.word = word

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_name = self.get_field_name(special)
        field_value = self.get_field_value()
        embed.add_field(
            name=field_name,
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

    def get_field_name(self, special: bool) -> str:
        return f'**{self.word}**' if not special else f'__**{self.word}** (일치)__'

    def get_field_value(self) -> str:
        pass


class Database:
    @staticmethod
    def is_duplicate(query: str, row: list) -> bool:
        return normalise(query) == normalise(row[0]) \
                   or any(normalise(query) in re.split(r'[,;] ', normalise(row[i])) for i in range(1, len(row)))

    def __init__(self, word_class: Type[Word], spreadsheet_key: str, sheet_number: int = 0):
        self.word_class = word_class

        self.credential = gspread.service_account(filename='res/google_credentials.json')
        self.sheet = self.credential.open_by_key(get_const(spreadsheet_key)).get_worksheet(sheet_number)

        self.last_reload = datetime.now()
        self.sheet_values = None
        self.reload()

    def reload(self):
        self.sheet_values = self.sheet.get_all_values()[self.word_class.leading_rows:]
        self.last_reload = datetime.now()
        return self

    def add_row(self, *values):
        self.sheet.insert_row(values, index=1, table_range='A1:I1')
        self.reload()

    def search_rows(self, query: str) -> Tuple[List[Word], set, bool]:
        """
        rows: 단어 목록

        duplicates: query와 뜻이나 단어 모양이 일치하는 단어 - 중요한 단어의 rows 내 index

        reloaded: 데이터베이스가 새로 로드되었는가

        :param query: 찾을 단어
        :return: rows, duplicates, reloaded
        """
        reloaded = False
        if self.last_reload + timedelta(weeks=1) < datetime.now():
            self.reload()
            reloaded = True
        duplicates = set()
        rows = list()
        for j, row in enumerate(self.sheet_values):
            for i, column in enumerate(row[:-self.word_class.back_slice] if self.word_class.back_slice else row):
                if normalise(query) in normalise(column):
                    # noinspection PyArgumentList
                    rows.append(self.word_class(*row))
                    break
            if self.is_duplicate(query, row):
                duplicates.add(len(rows) - 1)
        return rows, duplicates, reloaded


class DialectDatabase(Database):
    def __init__(self, word_class: Type[Word], spreadsheet_key: str, convert_function: Callable[[str], str]):
        self.convert_function = convert_function
        super().__init__(word_class, spreadsheet_key)

    def reload(self):
        self.sheet_values = self.sheet.get_all_values()[self.word_class.leading_rows:]
        for i, sheet_value in enumerate(self.sheet_values):
            self.sheet_values[i][0] = self.convert_function(sheet_value[0])
        self.last_reload = datetime.now()
        return self


class PosWord(Word):
    def __init__(self, word: str, pos: str, meaning: str, note: str = ''):
        super().__init__(word)
        self.pos = pos
        self.meaning = meaning
        self.note = note

    def get_field_name(self, special: bool) -> str:
        return (f'**{self.word}**' if not special else f'__**{self.word}** (일치)__') \
               + (f' [{self.note}]' if self.note else '')

    def get_field_value(self) -> str:
        return f'[{self.pos}] {self.meaning}'


class PosDatabase(Database):
    def __init__(self, spreadsheet_key: str, sheet_number: int = 0,
                 word_column: int = 0, pos_column: int = 1, meaning_column: int = 2, note_column: int = -1):
        super().__init__(PosWord, spreadsheet_key, sheet_number)
        self.word_column = word_column
        self.pos_column = pos_column
        self.meaning_column = meaning_column
        self.note_column = note_column

    def is_duplicate(self, query: str, row: list) -> bool:
        return normalise(query) == row[self.word_column] \
            or normalise(query) in re.split(r'[,;] ', normalise(row[self.meaning_column]))

    def search_rows(self, query: str) -> Tuple[List[Word], set, bool]:
        reloaded = False
        if self.last_reload + timedelta(weeks=1) < datetime.now():
            self.reload()
            reloaded = True
        duplicates = set()
        rows = list()
        for j, row in enumerate(self.sheet_values):
            if normalise(query) in normalise(row[self.word_column]) \
                    or normalise(query) in normalise(row[self.meaning_column]):
                # noinspection PyArgumentList
                rows.append(self.word_class(row[self.word_column], row[self.pos_column], row[self.meaning_column],
                                            '' if self.note_column == -1 else row[self.note_column]))
            if self.is_duplicate(query, row):
                duplicates.add(len(rows) - 1)
        return rows, duplicates, reloaded


if __name__ == '__main__':
    from database.zasok import ZasokeseWord

    zasokese_database = Database(ZasokeseWord, 'zasokese_database')
    zasokese_database.sheet.insert_row(['ariva', '으악', '', '', '', '', '', '선험', ''], index=2)
