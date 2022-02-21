import re
from datetime import datetime, timedelta
from typing import Tuple, Type, List

import gspread
from discord import Embed

from const import get_const
from util import normalise


class Word:
    back_slice = 0
    leading_rows = 1

    def __init__(self):
        pass

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        pass

    def get_field_value(self) -> str:
        pass


class ZasokeseWord(Word):
    back_slice = 2

    def __init__(self, word: str, noun: str = '', adj: str = '', verb: str = '', adv: str = '', prep: str = '',
                 conj: str = '', remark: str = '', derived_from_language: str = '', derived_from_word: str = ''):
        super().__init__()
        self.word = word
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.prep = prep
        self.conj = conj
        self.remark = remark
        self.derived_from_language = derived_from_language
        self.derived_from_word = derived_from_word

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_value = self.get_field_value()
        embed.add_field(
            name=f'**{self.word}**' if not special else f'__**{self.word}** (일치)__',
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명: {self.noun}')
        if self.adj:
            definitions.append(f'형: {self.adj}')
        if self.verb:
            definitions.append(f'동: {self.verb}')
        if self.adv:
            definitions.append(f'부: {self.adv}')
        if self.prep:
            definitions.append(f'관: {self.prep}')
        if self.conj:
            definitions.append(f'접: {self.conj}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


class ThravelemehWord(Word):
    back_slice = 2

    def __init__(self, word: str, noun: str = '', verb: str = '', adj: str = '', adv: str = '', conj: str = '',
                 remark: str = '', cont: str = '', origin: str = ''):
        super().__init__()
        self.word = word
        self.noun = noun
        self.verb = verb
        self.adj = adj
        self.adv = adv
        self.conj = conj
        self.remark = remark
        self.cont = cont
        self.origin = origin

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_value = self.get_field_value()
        embed.add_field(
            name=f'[{self.cont}] **{self.word}**' if not special else f'__[{self.cont}] **{self.word}** (일치)__',
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'[명] {self.noun}')
        if self.verb:
            definitions.append(f'[동] {self.verb}')
        if self.adj:
            definitions.append(f'[형] {self.adj}')
        if self.adv:
            definitions.append(f'[부] {self.adv}')
        if self.conj:
            definitions.append(f'[접] {self.conj}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


class BerquamWord(Word):
    def __init__(self, word: str, noun: str = '', adj: str = '', verb: str = '', adv: str = '', remark: str = ''):
        super().__init__()
        self.word = word
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.remark = remark

    def add_to_field(self, embed: Embed, special: bool = False) -> Embed:
        field_value = self.get_field_value()
        embed.add_field(
            name=f'**{self.word}**' if not special else f'__**{self.word}** (일치)__',
            value=field_value,
            inline=not (special or len(field_value) > 70)
        )
        return embed

    def get_field_value(self) -> str:
        definitions = list()
        if self.noun:
            definitions.append(f'명: {self.noun}')
        if self.adj:
            definitions.append(f'형: {self.adj}')
        if self.verb:
            definitions.append(f'동: {self.verb}')
        if self.adv:
            definitions.append(f'부: {self.adv}')
        if self.remark:
            definitions.append(f'비고: {self.remark}')
        return '\n'.join(definitions)


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
