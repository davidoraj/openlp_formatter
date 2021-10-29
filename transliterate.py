from googletrans import Translator
import re

song_text = """
ఈ జీవితం నీదే ప్రభు
సమర్పింతున్‌ నీకే (2)

1. నీ కొరకే జీవింతును 
ఉత్తమ సాక్షిగా (2)
ధైర్యముగా పయనింతును 
యేసుని మార్గములో (2)

2. జగతికి సందేశమునిత్తున్‌ 
యేసుక్రీస్తే ప్రభువని (2)
ఆయనే రక్షణ కర్తా 
నశియించు లోకానిక (2)

3. ప్రతికూల పరిస్థితులైనా 
స్థిరముగా నేనుందును (2)
యేసే నా రక్షకుడు 
అనుక్షణము కాపాడును (2)

4. చీకటి బ్రతుకును వీడుము 
జీవపు వెలుగును పొందుము (2)
కోరుము యేసుని నేడే 
నవజీవనమును నీకిచ్చున్‌ (2)
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
    'c': 'ch'
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
                output.append('\nVerse {}:'.format(fsplits[0].strip('().')))
                output.append(' '.join(fsplits[1:]).capitalize())
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
