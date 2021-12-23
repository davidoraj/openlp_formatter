from googletrans import Translator
import re

song_text = """
వింతైన తారక
వెలిసింది గగనాన
యేసయ్య జన్మస్థలము
చూపించు కార్యాన (2)
జ్ఞానులకే తప్పలేదు
ఆ తార అనుసరణ
దైవమే పంపెనని
గ్రహియించు హృదయాన (2)
మనమంతా జగమంతా
తారవలె క్రీస్తును చాటుదాం
హ్యాప్పీ క్రిస్మస్ మెర్రి క్రిస్మస్
వి విష్ యు హ్యాప్పీ క్రిస్మస్

1. ఆకాశమంతా ఆ దూతలంతా
గొంతెత్తి స్తుతి పాడగా
సర్వోన్నతమైన స్థలములలోన
దేవునికే నిత్య మహిమ (2)
భయముతో భ్రమలతో
ఉన్న గొర్రెల కాపరులన్
ముదముతో కలిసిరి
జనన వార్త చాటిరి

2. ఆ తూర్పు జ్ఞానులు ఆ గొర్రెల కాపరులు
యేసయ్యను దర్శించిరి
ఎంతో విలువైన కానుకలను అర్పించి
రారాజును పూజించిరి (2)
హేరోదుకు పుర జనులకు
శుభవార్త చాటిరి
అవనిలో వీరును
దూతలై నిలిచిరి
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

# print("Telugu Text:")
# print(song_text)
# print("\n\nOriginal Text:")
# print(translated)

translated = remove_accents(translated, replace)
translated = remove_accents(translated, replace2)
translated = format_text(translated)

print("\n\nFormatted Text:")
print(translated)
