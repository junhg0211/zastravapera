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

    def __init__(self):
        pass

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        pass

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

    def search_rows(self, query: str) -> Tuple[List[Word], set, bool]:
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
