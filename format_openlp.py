import re
import string
from collections import OrderedDict
import xml.dom.minidom

default_lines_per_slide = 4
section_lookup = {'V': 'Verse', 'C': 'Chorus', 'P': 'Pre-chorus', 'D': 'Bridge', 'T': 'Other', 'O': 'Other'}
sections = {'Verse', 'Chorus', 'Pre-chorus', 'Bridge', 'Tag', 'Instrumental', 'BREAK'}
ignore_section = {'BREAK'}
sections_regex = '|'.join(['^' + section + '[0-9 ]*:$' for section in sections])
repeat_section_regex = '|'.join(['^' + section + '[0-9 ]*' for section in sections])

# Variables used for creating song xml
verse_parts = list(string.ascii_lowercase)  # Creates ['a', 'b', 'c', ..., 'z']
line_delim = '<br/>'
section_delim = '<br/><br/>'

# c-chorus, n-verse, p-prechorus, b-bridge, c2

song_text = ""
with open('lyrics_10-24-21.txt', 'r') as lyricsfile:
    song_text = lyricsfile.readlines()


def is_section(line):
    if re.match(sections_regex, line):
        words = line.split()
        if len(words) > 1:
            return line.split()[0], line.split()[1].rstrip(':')
        else:
            return line.split()[0].rstrip(':'), 1
    else:
        return None, None


def is_repeat_Section(line):
    section = None
    id = 1
    if re.match(repeat_section_regex, line):
        words = line.split()
        section = words[0]
        if len(words) > 1:
            if re.match('[0-9]+', words[1]):
                id = words[1]
            else:
                id = '1'

    return section, id


# Parses the song from given annotated English and Telugu text
def get_song_annotated(one, two, lines_per_slide, title):
    sections = dict()
    order = []

    for line in one:
        if not line:
            continue

        section, id = is_section(line)
        rsection, rid = is_repeat_Section(line)
        if section:
            if section[0] == 'I':  # Instrumental
                sid = 'O' + str(id)
            else:
                sid = section[0] + str(id)
            if section not in ignore_section:
                order.append(sid)
        elif rsection:
            sid = rsection[0] + str(rid)
            if rsection not in ignore_section:
                order.append(sid)
            sid = None
        elif not sid:
            print('Missing song annotation at "{}"'.format(line))
        else:
            key = sid + '_one'
            content = sections.get(key, [])
            content.append(line)
            sections[key] = content

    section_map = set()
    i = 0
    for o in order:
        key = o + '_two'
        if key in section_map:
            continue

        while i < len(two):
            line = two[i]

            if line:
                content = sections.get(key, [])
                content.append(line)
                sections[key] = content
                i = i + 1
            else:
                section_map.add(key)
                i = i + 1
                break

    return {'sections': sections,
            'order': order,
            'verse_order': ' '.join(order),
            'lines_per_slide': lines_per_slide,
            'title': title}


# Parses the songs from text (list of lines)
def get_song_objects(song_lines_list):
    songs = []

    for song_lines in song_lines_list:
        line = song_lines[0][0]  # first line ---
        title = song_lines[0][1]  # second line
        one = song_lines[0][2:]
        two = song_lines[1]

        # Get lines per slide or default, (for next song)
        if re.match("---[0-9]+", line):
            lines_per_slide = int(line[3:])
        else:
            lines_per_slide = default_lines_per_slide

        # Parse song to object (based on annotations)
        song = get_song_annotated(one, two, lines_per_slide, title)

        # Create slides (English + Telugu combined)
        create_song_slide_deck(song)

        songs.append(song)

    return songs


def append_section_lyrics_xml(id, verse_part_counter, slides):
    counter = verse_part_counter.get(id, -1) + 1
    verse_part_counter[id] = counter
    vid = id.lower() + verse_parts[counter]
    return vid, slides[1:]


def append_section_slides(label, id, deck, section, lines_per_slide=default_lines_per_slide):
    # Init vars
    n = len(section)
    line_count = n if n < lines_per_slide else lines_per_slide
    i_last_slide = n if n % lines_per_slide == 0 else n - (n % lines_per_slide)  # index for last slide

    verse_part_counter = {}  # verse index (with alphabet counter, v1a, v1b etc)
    section_lyrics_dict = OrderedDict()

    # list of lines in a slide (added to given deck)

    # All but last slide (last n % lines_per_slide lines in the section)
    for i in range(0, i_last_slide, line_count):
        slides = []
        slides.append(label)
        for j in range(line_count):
            slides.append(section[j + i])

        vid, slide_lines = append_section_lyrics_xml(id, verse_part_counter, slides)
        section_lyrics_dict[vid] = slide_lines
        deck.append(slides)

    # Last slide for the section
    if i_last_slide < n:
        slides = []
        slides.append(label)
        for i in range(i_last_slide, n):
            slides.append(section[i])

        vid, slide_lines = append_section_lyrics_xml(id, verse_part_counter, slides)
        section_lyrics_dict[vid] = slide_lines
        deck.append(slides)

    return section_lyrics_dict


def merge_section_slides(main_deck, temp_deck, i):
    line_count = len(temp_deck[i])

    # for each line in a section
    for j in range(1, line_count):
        main_deck.append(temp_deck[i][j])


def merge_decks(deck1, deck2):
    # deck1 and deck2 lengths should be the same at this point
    deck = []
    n = len(deck1)

    # for each section
    for i in range(n):
        # add section label
        deck.append(deck1[i][0])
        merge_section_slides(deck, deck1, i)
        if deck2:
            deck.append("")  # empty line
            merge_section_slides(deck, deck2, i)

    return deck


# Takes two lists of tuples, and returns an OrderedDict of named lyrics (c1a->..., c1b->..., v1a->... etc.)
def merge_lyrics_xml(dict1, dict2):
    lyrics_xml = OrderedDict()

    for id in dict1.keys():
        xml_string = line_delim.join(dict1[id])
        if dict2:
            xml_string = xml_string + section_delim + line_delim.join(dict2[id])
        lyrics_xml[id] = xml_string

    return lyrics_xml


# Given an annotated song (sections/order)
# it returns the slides for the song (English & Telugu)
def create_song_slide_deck(song):
    section_map = set()
    deck1 = []  # english
    deck2 = []  # telugu
    lyrics1_xml_dict = OrderedDict()
    lyrics2_xml_dict = OrderedDict()

    for o in song['order']:
        one = o + '_one'
        two = o + '_two'
        if one in song['sections']:
            section1 = song['sections'][one]
        if two in song['sections']:
            section2 = song['sections'][two]
        else:
            section2 = None

        n = len(section1)

        # Validation
        if section2 and n != len(section2):
            raise SyntaxError("Lines don't match for song: " + str(song))

        label = '---[{sec}:{id}]---'.format(sec=section_lookup[o[0]], id=o[1])

        # skip duplicate section
        if label in section_map:
            continue
        else:
            section_map.add(label)

        # Convert a section (with n lines) to k slides, and put in a dict with vid (verse id) as key
        lyrics1_xml_dict.update(append_section_slides(label, o, deck1, section1, song['lines_per_slide']))
        if section2:
            lyrics2_xml_dict.update(append_section_slides(label, o, deck2, section2, song['lines_per_slide']))

    # Merge decks into a a single deck (song text in "edit-all")
    song['deck'] = merge_decks(deck1, deck2)

    # Merge lyrics xml for song import
    song['lyrics_xml'] = merge_lyrics_xml(lyrics1_xml_dict, lyrics2_xml_dict)

    return


# Returns list of tuples (englist_lines_list, optional_telugu_lines_list)
def get_song_lines(lines):
    song_lines_list = []
    one = []
    two = []
    curlist = None

    for i in range(len(lines)):
        line = lines[i]
        line = line.strip().strip("\n")
        if line.startswith("---"):
            if one:
                song_lines_list.append((one, two))
            one = []
            two = []
            curlist = one
            curlist.append(line)
        elif line == "--":
            curlist = two
        elif line:
            curlist.append(line)
        elif curlist is not None:
            curlist.append("")

    return song_lines_list


def get_xml(tag, text, props=''):
    return '<{tag} {props}>{text}</{tag}>'.format(tag=tag, text=text, props=props)


def save_to_xml(song):
    start = """<?xml version='1.0' encoding='UTF-8'?>
<song xmlns="http://openlyrics.info/namespace/2009/song" version="0.8" createdIn="OpenLP 2.4.6" modifiedIn="OpenLP 2.4.6">"""

    properties_text = \
        get_xml('titles', get_xml('title', song['title'])) + \
        get_xml('authors', get_xml('author', 'Unknown')) + \
        get_xml('verseOrder', song['verse_order'].lower())
    properties = '\n' + get_xml('properties', properties_text) + '\n'

    # Create a list of verses with name=verse_id
    # song['lyrics_xml'] is an ordered dict with key=verse_id, value=[slide-lyrics]
    lyrics_xml_list = []
    for vid in song['lyrics_xml']:
        verse_lines = get_xml('lines', ''.join(song['lyrics_xml'][vid]))
        lyrics_xml_list.append(get_xml('verse', verse_lines, 'name="{}"'.format(vid)))
    end = "\n</song>"

    # Put combine xml content into one string
    song_xml = start + properties + get_xml('lyrics', '\n'.join(lyrics_xml_list)) + end

    # Write to file
    with open(song['title'] + '.xml', 'w') as xml_file:
        # TODO: Find a way to pretty print without disturbing verse lines text
        # xml_file.write(xml.dom.minidom.parseString(song_xml).toprettyxml())
        xml_file.write(song_xml)


def main():
    # Split songs lines to a list
    song_lines_list = get_song_lines(song_text)

    # Parse all the songs (returns a list of song objects)
    songs = get_song_objects(song_lines_list)

    # Create slides
    for song in songs:

        # Export to xml
        save_to_xml(song)

        # Print text
        print("----------------------------------")
        print(song['verse_order'])
        for line in song['deck']:
            print(line)


if __name__ == "__main__":
    main()
