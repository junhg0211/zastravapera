from database import Word


class IremnaWord(Word):
    def __init__(self, word: str, pronunciation: str, pos: str, meaning: str,
                 word2: str, pronunciation2: str, pos2: str, meaning2: str, 
                 word3: str, pronunciation3: str, pos3: str, meaning3: str, 
                 word4: str, *notes: str):
        super().__init__(word)
        self.pronunciation = pronunciation
        self.pos = pos
        self.meaning = meaning
        
        self.word2 = word2
        self.pronunciation2 = pronunciation2
        self.pos2 = pos2
        self.meaning2 = meaning2
        
        self.word3 = word3
        self.pronunciation3 = pronunciation3
        self.pos3 = pos3
        self.meaning3 = meaning3
        
        self.word4 = word4
        self.notes = notes

    def get_field_value(self) -> str:
        definitions = list()
        if self.meaning:
            line = ''
            if self.pos:
                line += '<' + self.pos + '> '
            line += self.meaning
            definitions.append(line)
        if self.word2:
            line = '→ '
            if self.pos2:
                line += '<' + self.pos2 + '> '
            line += '**' + self.word2 + '**'
            if self.pronunciation2:
                line += ' [' + self.pronunciation2 + ']'
            if self.meaning2:
                line += ' ' + self.meaning2
            definitions.append(line)
        if self.word3:
            line = '→ '
            if self.pos3:
                line += '<' + self.pos3 + '> '
            line += '**' + self.word3 + '**'
            if self.pronunciation3:
                line += ' [' + self.pronunciation3 + ']'
            if self.meaning3:
                line += ' ' + self.meaning3
            definitions.append(line)
        return '\n'.join(definitions)
