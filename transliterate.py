from googletrans import Translator
import re
import argparse

# Read telugu text from file
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help="Path to file containing Telugu text for translation")
args = parser.parse_args()

song_text = ""
with open(args.input, 'r') as telugu_text:
    song_text = ''.join(telugu_text.readlines())

replace = {
    'ā': 'aa',
    'cc': 'c',
    'c\'h': 'c',
    'ḍ': 'd',
    'd\'d': 'dd',
    'ē': 'e',
    'ī': 'ee',
    'jñ': 'gn',
    'ḷ': 'l',
    'ṁ': 'm',
    'm̐': 'm',
    'm\'m': 'mm',
    'ṇ': 'n',
    'n\'y': 'ny',
    'ṅ': 'n',
    'n̄': 'n',
    'ō': 'o',
    'r̥': 'ru',
    'ṟ': 'r',
    'ś': 's',
    'ṣ': 'sh',
    'ṭ': 't',
    'ū': 'u',
    'ū': 'u',
    '-': '',
    '–': '',
    '  ': ' ',
    '   ': ' ',
    '‌': '',
}

replace2 = {
    'c': 'ch',
    'sv': 'sw',
    'stuti': 'sthuti'
}


def remove_accents(translated, rmap):
    for c in rmap.keys():
        r = rmap[c]
        C = c.capitalize()
        R = r.capitalize()
        translated = translated.replace(c, r).replace(C, R)

    return translated


def format_text(text):
    lines = text.split('\n')
    output = []
    for line in lines:
        formatted = line.strip()
        if len(formatted) > 0:
            if re.match('^[0-9]+', formatted):
                fsplits = formatted.split(' ')
                vid = fsplits[0].strip('().')
                output.append('\nVerse {}:'.format(vid))
                # output.append('')
                output.append(vid + '. ' + ' '.join(fsplits[1:]).capitalize())
            else:
                output.append(formatted.capitalize())

    return '\n'.join(output)


translated = ""

translator = Translator()
translated = translator.translate(song_text, dest="en").extra_data['origin_pronunciation']

translated = remove_accents(translated, replace)
translated = remove_accents(translated, replace2)
translated = format_text(translated)

print("\n\n---")
print(translated.split('\n')[0].title())  # Title
print("Chorus:")
print(translated)
print("--")
print(song_text)
print("---")
