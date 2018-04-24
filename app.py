# -*- coding: utf-8 -*-

import more_itertools as mit
from operator import itemgetter
from library.google_translate import translate_text
from functools import lru_cache
import os.path as path


class Translate:
    def __init__(self):
        self.katakana_chart = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヽヾ"
        self.hiragana_chart = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖゝゞ"

    def hiragana_to_katakana(self):
        return str.maketrans(self.hiragana_chart, self.katakana_chart)

    def katakana_to_hiragana(self):
        return str.maketrans(self.katakana_chart, self.hiragana_chart)


# not used yet
translator = Translate()



filepath = './data/test.txt'


@lru_cache(maxsize=1024)
def translate_katakana(filepath, output=True):
    with open(filepath) as text:
        full_text = text.read()
        output_text = full_text
        #print(full_text)

        #print('translated below')

        #translated = full_text.translate(translator.hiragana_to_katakana())
        #print(translated)

        word_indices = []
        word_chars = []
        for i, word in enumerate(full_text):
            if word in translator.katakana_chart:
                word_indices.append(i)
                word_chars.append(word)

        grouped_indices = mit.consecutive_groups(word_indices)
        grouped_indices = [list(word) for word in grouped_indices]

        words_to_translate = []
        for word_groups_i in grouped_indices:
            #print(list(word_groups_i))

            word_to_translate = []
            for i in word_groups_i:
                word_to_translate.append(full_text[i])

            word_to_translate = ''.join(word_to_translate)
            translated_word = translate_text('en', word_to_translate, verbose=False)['translatedText']

            print('translating {0} to {1}'.format(word_to_translate, translated_word))

            output_text = output_text.replace(word_to_translate, translated_word)

        if output == True:
            output_filepath = '{0}{1}'.format(path.splitext(filepath)[0], '_output.txt')
            with open(output_filepath, 'w') as output_file:
                # dump entire string into file
                output_file.write(output_text)

        print('\noutput:')
        print(output_text)


translate_katakana(filepath, output=True)
