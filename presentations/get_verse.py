import xmltodict
import tkinter as tk


# def get_bible_verse():
#     reference = entry.get()
#     if reference:
#         verse_text.set(fetch_verse_to_ui(reference))

def fetch_verse_to_ui():
    reference = entry.get()
    if reference:
        ref = print_reference(reference)
        text = (ref + '\n' + print_verse(reference, bible_text=bible_text_nkjv) + '\n\n' +
                print_verse(reference, bible_text=bible_text_telugu))
        verse_text.set(text)
        with open('verse_out.txt', 'w') as vfile:
            vfile.writelines(text)


# Create main window
root = tk.Tk()
root.title("Bible Verse Fetcher")

# Input field
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Button to fetch verse
button = tk.Button(root, text="Get Verse", command=fetch_verse_to_ui)
button.pack(pady=5)

# Label to display verse
verse_text = tk.StringVar()
label = tk.Label(root, textvariable=verse_text, wraplength=300, justify="center")
label.pack(pady=10)

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
            short_form_lookup[short[:-1].lower()] = book
        else:
            book = short.strip()
            short_form_lookup[book.lower()] = book

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
    book = reference[:i].strip().lower()
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
    ref = f'{get_book_from_reference(reference)} {get_chapter_verse_from_reference(reference)}'
    print(ref)
    return ref


def print_verse(reference, bible_text):
    # debug
    text = get_reference(reference, bible_text)
    text = get_formatted_text(text)
    print(text)
    print()
    return text


def main():
    init()
    print_verse('John 1:21', bible_text=bible_text_nkjv)
    print_verse('John 1:21', bible_text=bible_text_telugu)

    # # Test with nbbc verse list
    # with open('/Users/david_ogirala/git-repos/misc_tools/scraper/nbbc/verses.txt', 'r') as vfile:
    #     for v in vfile.readlines():
    #         print_verse(v.strip(), bible_text=bible_text_nkjv)
    #         print_verse(v.strip(), bible_text=bible_text_telugu)

    # # Run GUI
    root.mainloop()


if __name__ == "__main__":
    main()
