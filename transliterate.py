from googletrans import Translator
import re

song_text = """
స్తుతియు మహిమ ఘనత నీకే
యుయుగముల వరకు
ఎంతో నమ్మదగిన దేవా
ఎంతో నమ్మదగిన దేవా

1. మా దేవుడవై మాకిచ్చితివి
ఎంతో గొప్ప శుభదినము (2)
మేమందరము ఉత్సహించి
సంతోషించెదము (2)
కొనియాడెదము మరువబడని
మేలులు జేసెనని (2)

2. నీ వొక్కడవే గొప్ప దేవుడవు
ఘన కార్యములు చేయుదువు (2)
నీదు కృపయే నిరంతరము
నిలిచియుండునుగా (2)
నిన్ను మేము ఆనందముతో
ఆరాధించెదము (2)

3. నూతనముగా దినదినము నిలుచు
నీదు వాత్సల్యత మా పై (2)
ఖ్యాతిగా నిలిచే నీ నామమును
కీర్తించెదమెప్పుడు (2)
ప్రీతితో మా స్తుతులర్పించెదము
దాక్షిణ్య ప్రభువా (2)

4. నీవె మాకు పరమ ప్రభుడువై
నీ చిత్తము నెరవేర్చితివి (2)
జీవమునిచ్చి నడిపించితివి
నీ ఆత్మద్వారా (2)
నడిపించెదవు సమ భూమిగల
ప్రదేశములో నన్ను (2)

5. భరియించితివి శ్రమలు నిందలు
ఓర్చితివన్ని మా కొరకు (2)
మరణము గెల్చి ఓడించితివి
సాతాను బలమున్ (2)
పరము నుండి మాకై వచ్చే
ప్రభు యేసు జయము (2)
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
