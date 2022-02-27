from googletrans import Translator
import re

song_text = """
ప్రభువా గురి యెద్దకే
పరిగెత్తుచున్నాను నేను (2)
ఉన్నత పిలుపునకు కలుగు
బహుమానము పొందవలెనని (2)

1. ఏవేవీ లాభకరములై యుండెనో
వాటిని క్రీస్తునిమిత్తం (2)
నష్టముగా ఎంచుకొని
ముందుకే సాగుచున్నాను (2)

2. క్రీస్తును సంపాదించుకొని
తన పునరుధ్ధాన బలమును (2)
ఎరిగి ఆయన శ్రమలలో
పాలివాడనౌదున్ (2)

3. వెనుకున్న వన్నియు మరచి
ముందున్న వాటి కొరకై (2)
వేగిరపడుచు ధైర్యముగా
ముందుకుసాగుచున్నాను (2)
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
print("INSERT_TITLE")
print("Chorus:")
print(translated)
print("--")
print(song_text[1:-1])
print("---")
