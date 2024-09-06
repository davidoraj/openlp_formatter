#!/usr/bin/env python3

from googletrans import Translator
import re
import argparse
import time

song_text = ""


def read_args():
    global song_text

    # Read telugu text from file
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="telugu.txt", required=False,
                        help="Path to file containing Telugu text for translation")
    parser.add_argument("--text", type=str, default="", required=False,
                        help="Song text")
    args = parser.parse_args()

    if args.text:
        song_text = args.text
    else:
        with open(args.input, 'r', encoding='utf-8') as telugu_text:
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


def translate(song_text):
    translated = ""
    try:
        translator = Translator()
        translated = translator.translate(song_text, dest="en").extra_data['origin_pronunciation']

        translated = remove_accents(translated, replace)
        translated = remove_accents(translated, replace2)
        translated = format_text(translated)
    except:
        time.sleep(1)
        print('retrying translate for song text below:')
        return translate(song_text)

    return translated


def print_song(translated, song_text):
    print("\n\n---")
    print(translated.split('\n')[0].title())  # Title
    print("Chorus:")
    print(translated)
    print("--")
    print(song_text)
    print("---")


def write_to_file(translated, song_text, file_name, metadata):
    with open(file_name, 'w') as file:
        file.write("---\n")
        # file.write(translated.split('\n')[0].title())  # Title
        file.write(file_name.split('/')[1].split('.')[0]) # title
        if metadata:
            file.write(f'\n{metadata}')
        file.write("\nChorus:\n")
        file.writelines(translated)
        file.write("\n--\n")
        file.writelines(song_text)
        file.write("\n---\n")


def main():
    read_args()
    print_song(translate(song_text), song_text)


if __name__ == "__main__":
    main()
