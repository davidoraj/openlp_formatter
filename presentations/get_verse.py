import xmltodict

short_form_lookup = {}
book_index_lookup = {}
bible_text_nkjv = dict()
bible_text_telugu = dict()


def init():
    global bible_text_nkjv
    global bible_text_telugu

    with(open('bibles/short.txt', 'r')) as shorts_file:
        short_forms = shorts_file.readlines()

    # Init short forms for lookup
    book = short_forms[0].strip()
    for short in short_forms:
        short = short.strip()
        if short.endswith('.'):
            short_form_lookup[short[:-1]] = book
        else:
            book = short.strip()
            short_form_lookup[book] = book

    # Load english and telugu bibles
    with open("bibles/NKJV.xml", "r") as file:
        bible_text_nkjv = xmltodict.parse(file.read())
    with open("bibles/TELUGU_2.xml", "r") as file:
        bible_text_telugu = xmltodict.parse(file.read())

    # Get indices for each book
    i = 0
    for b in bible_text_nkjv['bible']['b']:
        name = b['@n']
        book_index_lookup[name] = i
        i = i + 1


def get_book_from_reference(reference):
    i = reference.rfind(' ')
    book = reference[:i].strip()
    book = short_form_lookup[book]
    return book


def get_chapter_verse_from_reference(reference):
    i = reference.rfind(' ')
    chapter_verse = reference[i + 1:]
    return chapter_verse


def get_reference(reference, bible_text):
    book = get_book_from_reference(reference)
    chapter_verse = get_chapter_verse_from_reference(reference)

    cv = chapter_verse.split(':')
    chapter = int(cv[0]) - 1
    verses = cv[1].split('-')
    verse_start = int(verses[0]) - 1
    verse_end = (verse_start + 1 if len(verses) == 1 else int(verses[1]))

    book_index = book_index_lookup[book]
    try:
        chapter_object = bible_text['bible']['b'][book_index]['c']

        if isinstance(chapter_object, list):
            # If there's more than 1 chapters
            text = bible_text['bible']['b'][book_index]['c'][chapter]['v'][verse_start:verse_end]
        else:
            # If is only 1 chapter
            text = bible_text['bible']['b'][book_index]['c']['v'][verse_start:verse_end]

        if len(text) > 0:
            print_reference(reference)
        else:
            print('Try again')
        return text
    except:
        print('ERROR!')
        return ''


def get_formatted_text(text):
    verse_list = []
    for verse in text:
        verse_number = verse['@n']
        verse_text = verse['#text']
        verse_list.append(f'{verse_number} {verse_text}')

    return '\n'.join(verse_list)


def print_reference(reference):
    print(f'{get_book_from_reference(reference)} {get_chapter_verse_from_reference(reference)}')


def print_verse(reference, bible_text):
    # debug

    text = get_reference(reference, bible_text)
    text = get_formatted_text(text)
    print(text)
    print()


def main():
    init()
    print_verse('John 1:21', bible_text=bible_text_nkjv)
    print_verse('John 1:21', bible_text=bible_text_telugu)

    # # Test with nbbc verse list
    # with open('/Users/david_ogirala/git-repos/misc_tools/scraper/nbbc/verses.txt', 'r') as vfile:
    #     for v in vfile.readlines():
    #         print_verse(v.strip(), bible_text=bible_text_nkjv)
    #         print_verse(v.strip(), bible_text=bible_text_telugu)


if __name__ == "__main__":
    main()
