from googletrans import Translator
import re

song_text = """
అన్ని నామముల
కన్న పై నామము
యేసుని నామము
ఎన్ని తరములకైనా
ఘనపరచ దగినది
క్రీస్తేసు నామము

యేసు నామము జయం జయము
సాతాను శక్తుల్ లయం లయము (2)
హల్లెలూయ ఆమెన్ హల్లెలూయా
హల్లెలూయా ఆమెన్ (2)

1. పాపముల నుండి విడిపించును
యేసుని నామము (2)
నిత్య నరకాగ్నిలో నుండి రక్షించును
క్రీస్తేసు నామము (2)

2. సాతాను పై అధికార మిచ్చును
శక్తి గల యేసు నామము (2)
శత్రు సమూహము పై జయమునిచ్చును
జయశీలుడైన యేసు నామము (2)
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
