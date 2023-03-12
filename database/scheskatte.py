from database import Word


class ScheskatteWord(Word):
    def __init__(self, word: str, noun: str = '', adj: str = '', verb: str = '', adv: str = '', prep: str = '',
                    remark: str = '', derived_from_language: str = '', derived_from_word: str = ''):
        super().__init__(word)
        self.noun = noun
        self.adj = adj
        self.verb = verb
        self.adv = adv
        self.prep = prep
        self.remark = remark
        self.derived_from_language = derived_from_language
        self.derived_from_word = derived_from_word

    def get_field_name(self, special: bool) -> str:
        return (f'**{self.word}**' if not special else f'__**{self.word}** (일치)__') \
               + (f' [{self.note}]' if self.note else '')

    def get_field_value(self) -> str:
        return self.meaning