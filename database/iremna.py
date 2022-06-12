from copy import copy

from database import Word


class IremnaWord(Word):
    def __init__(self, *cells: str):
        super().__init__(cells[0])
        self.cells = cells

    def sliding_window(self):
        cells = list(copy(self.cells))
        while cells:
            result, cells = cells[:4], cells[4:]
            while len(result) < 4:
                result.append('')
            yield result

    def get_field_value(self) -> str:
        definitions = list()
        for i, window in enumerate(self.sliding_window()):
            word, pronunciation, pos, meaning = window
            if not word:
                break
            line = '→ ' if i else ''
            if pos:
                line += f'<{pos}> '
            if i:
                line += f'**{word}**'
                if pronunciation:
                    line += f' [{pronunciation}]'
                line += f' {meaning}'
            else:
                line += meaning
            definitions.append(line)
        return '\n'.join(definitions)
