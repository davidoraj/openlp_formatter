import re

default_lines_per_slide = 4
section_lookup = {'V': 'Verse', 'C': 'Chorus', 'P': 'Pre-chorus', 'D': 'Bridge', 'T': 'Other', 'O': 'Other'}
sections = {'Verse', 'Chorus', 'Pre-chorus', 'Bridge', 'Tag', 'Instrumental', 'BREAK'}
ignore_section = {'BREAK'}
sections_regex = '|'.join(['^' + section + '[0-9 ]*:$' for section in sections])
repeat_section_regex = '|'.join(['^' + section + '[0-9 ]*' for section in sections])

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
            if section[0] == 'I':
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

    return {'sections': sections, 'order': order, 'lines_per_slide': lines_per_slide, 'title': title}


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

        song = get_song_annotated(one, two, lines_per_slide, title)
        songs.append(song)

    return songs


def append_section_slides(label, deck, section, lines_per_slide=default_lines_per_slide):
    # Init vars
    n = len(section)
    line_count = n if n < lines_per_slide else lines_per_slide
    i_last_slide = n if n % lines_per_slide == 0 else n - (n % lines_per_slide)  # index for last slide

    # list of lines in a slide (added to given deck)

    # All but last slide (last n % lines_per_slide lines in the section)
    for i in range(0, i_last_slide, line_count):
        slides = []
        slides.append(label)
        for j in range(line_count):
            slides.append(section[j + i])
        deck.append(slides)

    # Last slide for the section
    if i_last_slide < n:
        slides = []
        slides.append(label)
        for i in range(i_last_slide, n):
            slides.append(section[i])
        deck.append(slides)

    return


def merge_section_slides(main_deck, temp_deck, i):
    line_count = len(temp_deck[i])

    # for each line in a section
    for j in range(1, line_count):
        main_deck.append(temp_deck[i][j])


def merge_decks(deck1, deck2, order):
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

    return deck, ' '.join(order)


# Given an annotated song (sections/order)
# it returns the slides for the song (English & Telugu)
def get_song_slide_deck(song):
    section_map = set()
    deck1 = []  # english
    deck2 = []  # telugu
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

        append_section_slides(label, deck1, section1, song['lines_per_slide'])
        if section2:
            append_section_slides(label, deck2, section2, song['lines_per_slide'])

    # Merge decks into a a single deck
    return merge_decks(deck1, deck2, song['order'])


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
    return '<{tag}{props}>{text}</{tag}>'.format(tag=tag, text=text, props=props)


def save_to_xml(song, deck, order):
    start = """
    <?xml version='1.0' encoding='UTF-8'?>
    <song xmlns="http://openlyrics.info/namespace/2009/song" version="0.8" createdIn="OpenLP 2.4.6" modifiedIn="OpenLP 2.4.6">
    """
    properties_text = \
        get_xml('titles', get_xml('title', song['title'])) + \
        get_xml('authors', get_xml('author', 'Unknown')) + \
        get_xml('verseOrder', order.lower())
    properties = get_xml('properties', properties_text)

    lyrics_text = ''
    lyrics = get_xml('lyrics', lyrics_text)
    end = "</song>"

    return start + properties + lyrics + end


def main():
    # Split songs lines to a list
    song_lines_list = get_song_lines(song_text)

    # Parse all the songs (returns a list of song objects)
    songs = get_song_objects(song_lines_list)

    # Create slides
    for song in songs:
        deck, order = get_song_slide_deck(song)

        # Export to xml
        save_to_xml(song, deck, order)

        print("----------------------------------")
        print(' '.join(order.split()))
        for line in deck:
            print(line)


if __name__ == "__main__":
    main()
