import random
from new_package.thravelemeh import pool


class WordGenerator:
    def __init__(self, length=5, amount=10, countable=True):
        self.length = length
        self.amount = amount
        self.countable = countable
        self.result = []

    def random_length(self):
        self.length = random.randint(2, 8)

    def make_word(self):
        word = ''
        last_added = ''

        # set random length
        self.random_length()

        # generate word
        for i in range(self.length):
            # first character
            if not i:
                last_added = random.choice(pool.alls)

            # last character
            elif i == self.length - 1:
                # if uncountable
                if not self.countable:
                    last_added = 'h'
                # if countable
                else:
                    # last was son
                    if last_added not in pool.lmnhs and last_added in pool.sons:
                        last_added = random.choice(pool.last_locatable_mothers)
                    # last was mother
                    else:
                        while True:
                            last_addable = random.choice(pool.last_locatables)
                            if last_added != last_addable:
                                last_added = last_addable
                                break

            # middle character
            else:
                # last was son
                if last_added not in pool.lmnhs and last_added in pool.sons:
                    last_added = random.choice(pool.mothers_with_h)
                # last was mother
                else:
                    while True:
                        last_addable = random.choice(pool.alls)
                        if last_added != last_addable:
                            last_added = last_addable
                            break

            # add last letter
            word += last_added

            # set double mothers
            if last_added == 'w':
                last_added = random.choice(['a', 'e', 'i'])
                word += last_added
            elif last_added == 'y':
                last_added = random.choice(['a', 'e', 'o', 'u'])
                word += last_added

        # set contrast
        if len(word) == 2 and word[0] in pool.mothers:
            word = 'v' + word
        elif len(word) == 4 and word[0] in pool.mothers:
            word = 'j' + word
        elif len(word) == 6 and word[0] in pool.mothers:
            word = 'q' + word

        # change to double mothers
        if 'ia' in word:
            word = word.replace('ia', 'ya')
        if 'ie' in word:
            word = word.replace('ie', 'ye')
        if 'iu' in word:
            word = word.replace('iu', 'yu')
        if 'io' in word:
            word = word.replace('io', 'yo')
        if 'ua' in word:
            word = word.replace('ua', 'wa')
        if 'ue' in word:
            word = word.replace('ue', 'we')
        if 'ui' in word:
            word = word.replace('ui', 'wi')

        # fix finally
        if 'x' in word:
            if word[0] == 'x':
                word = word.replace(word[0], 'z')
            for i in range(len(word)):
                if i >= 1 and word[i-1] in pool.lmnhs and word[i] == 'x':
                    word = word.replace(word[i], 'z')

        # reset
        if word[0] in pool.lmnhs and word[1] in pool.sons:
            return self.make_word()

        lmnh_count = 0
        for letter in word:
            if letter in pool.lmnhs:
                lmnh_count += 1
            else:
                if lmnh_count >= 2 and letter in pool.sons:
                    return self.make_word()
                else:
                    lmnh_count = 0

        for banned_string in pool.forbidden:
            if banned_string in word:
                return self.make_word()
        self.result.append(word)

    def generate_words(self):
        self.result.clear()
        for i in range(self.amount):
            self.make_word()
        return self.result
