import xmltodict

import xml.etree.ElementTree as ET

with open('bibles/Telugu.xml', 'r') as tfile:
    bible_text = xmltodict.parse(tfile.read())

bookslist = bible_text['cesDoc']['text']['body']['div']

# Create root element
bible = ET.Element("bible")

for bookobj in bookslist:
    # Add a book element
    book = ET.SubElement(bible, "b", {"n": f'{bookobj['@id']}'})

    chapter_id = 1
    chapters = []
    if isinstance(bookobj['div'], dict):
        chapterobj = bookobj['div']
        chapters.append(chapterobj)
    else:
        chapters = bookobj['div']

    for chapterobj in chapters:
        # Add a chapter element
        chapter = ET.SubElement(book, "c", {"n": f'{chapter_id}'})
        chapter_id = chapter_id + 1

        verse_id = 1
        for verseobj in chapterobj['seg']:
            # Add a verse element
            if '#text' in verseobj:
                verse = ET.SubElement(chapter, "v", {"n": f'{verse_id}'})
                verse.text = verseobj['#text']
                verse_id = verse_id + 1

# Convert to an XML string
xml_string = ET.tostring(bible, encoding="unicode")

with open('bibles/TELUGU_2.xml', 'w') as tufile:
    tufile.write(xml_string)
