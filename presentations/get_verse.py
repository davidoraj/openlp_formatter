import xmltodict

short_form_lookup = {}
book_index_lookup = {}
bible_text = dict()


def init():
    global bible_text

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

    # Get indices of book names
    with open("bibles/NKJV.xml", "r") as file:
        bible_text = xmltodict.parse(file.read())
    i = 0
    for b in bible_text['bible']['b']:
        name = bible_text['bible']['b'][i]['@n']
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


def get_reference(reference):
    book = get_book_from_reference(reference)
    chapter_verse = get_chapter_verse_from_reference(reference)

    cv = chapter_verse.split(':')
    chapter = int(cv[0]) - 1
    verses = cv[1].split('-')
    verse_start = int(verses[0]) - 1
    verse_end = (verse_start + 1 if len(verses) == 1 else int(verses[1]))

    book_index = book_index_lookup[book]
    try:
        text = bible_text['bible']['b'][book_index]['c'][chapter]['v'][verse_start:verse_end]
        return text
    except:
        text = bible_text['bible']['b'][book_index]['c']['v'][verse_start:verse_end]
        return text


def get_formatted_text(text):
    verse_list = []
    for verse in text:
        verse_number = verse['@n']
        verse_text = verse['#text']
        verse_list.append(f'{verse_number} {verse_text}')

    return '\n'.join(verse_list)


def print_reference(reference):
    print(f'{get_book_from_reference(reference)} {get_chapter_verse_from_reference(reference)}')


def print_verse(reference):
    # debug
    print_reference(reference)
    text = get_reference(reference)
    text = get_formatted_text(text)
    print(text)
    print()


def main():
    init()
    # print(short_form_lookup)
    # print(book_index_lookup)
    # print_verse('1 John 3:15-16')
    # print_verse('John 3:16')
    # print_verse('Jn 8:32')
    # print_verse('Ps 118:24-26')
    # print_verse('Jude 1:20-21')

    with open('/Users/david_ogirala/git-repos/misc_tools/scraper/nbbc/verses.txt', 'r') as vfile:
        for v in vfile.readlines():
            print_verse(v.strip())


if __name__ == "__main__":
    main()
