from googletrans import Translator
import re

song_text = """
దైవం ప్రేమ స్వరూపం
ప్రేమకు భాష్యం శ్రీయేసుడే
అవనిలొ దైవం ప్రేమ స్వరూపం
ప్రేమకు భాష్యం శ్రీయేసుడే

ప్రేమే త్యాగభరితం
సిలువలో దివ్య చరితం (2)

1. ఈ ధరలో ప్రేమ శూన్యం
ఆదరణ లేని గమ్యం (2)
మధురంపు యేసు ప్రేమ
మదినింపు మదుర శాంతి (2)

2. కరుణించి క్రీస్తు నీకై
మరణించె సిలువ బలియై (2)
పరలోక దివ్య ప్రేమన్‌
ధరనిచ్చె నిన్ను బ్రోవన్‌ (2)
"""

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
    '-': '',
    '–': '',
    '  ': ' ',
    '   ': ' ',
    '‌': '',
}

replace2 = {
    'c': 'ch',
    'svar': 'swar'
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
                output.append(vid + '. ' + ' '.join(fsplits[1:]).capitalize())
            else:
                output.append(formatted.capitalize())

    return '\n'.join(output)


translated = ""

translator = Translator()
translated = translator.translate(song_text, dest="en").extra_data['origin_pronunciation']

# print("Telugu Text:")
# print(song_text)
# print("\n\nOriginal Text:")
# print(translated)

translated = remove_accents(translated, replace)
translated = remove_accents(translated, replace2)
translated = format_text(translated)

print("\n\nFormatted Text:")
print(translated)
