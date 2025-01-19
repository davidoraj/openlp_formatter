# Replace   

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT, MSO_VERTICAL_ANCHOR, MSO_UNDERLINE
from itertools import takewhile
import re

width = 1280
height = 350
margin = 20

green_color = RGBColor(0, 200, 0)
black_color = RGBColor(50, 50, 50)
white_color = RGBColor(245, 245, 245)
title_font = 36
content_font = 28
font_spacing = 1.1
font_name = 'Arial'

title_height = margin + title_font
content_position = margin + title_height
content_height_1 = height - 2 * margin
content_height_2 = height - 2 * margin - title_height
textbox_width = width - 2 * margin

# Define patterns for bold, italic, and underline
patterns = [
    (r"\*(.*?)\*", {"bold": True}),  # Bold: *text*
    (r"_(.*?)_", {"italic": True}),  # Italic: _text_
    (r"__(.*?)__", {"underline": MSO_UNDERLINE.SINGLE_LINE}),  # Underline: __text__
    (r"[1-3]*[ ]*[Song of]*[A-Za-z]*[ ][1-9]+:[0-9-,]*", {"bold": True})
]


def create_presentation(width, height):
    presentation = Presentation()
    presentation.slide_width = Pt(width)
    presentation.slide_height = Pt(height)
    return presentation


def new_slide(presentation):
    # 0. Title (presentation title slide)
    # 1. Title and Content
    # 2. Section Header (sometimes called Segue)
    # 3. Two Content (side by side bullet textboxes)
    # 4. Comparison (same but additional title for each side by side content box)
    # 5. Title Only
    # 6. Blank
    # 7. Content with Caption
    # 8. Picture with Caption
    slide = presentation.slides.add_slide(presentation.slide_layouts[6])

    # Add bg color
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = black_color

    # Add bg image
    # slide.shapes.add_picture(background_image_path, Inches(0), Inches(0), Inches(9), Inches(6))

    return slide


def is_title(line):
    return line.startswith('#')


def get_indent(line):
    n = count_leading_spaces(line)
    if n % 2 != 0:
        raise RuntimeError(f'Remove extra space at "{line}"')
    return int(n / 2)


def count_leading_spaces(s):
    return sum(1 for _ in takewhile(lambda x: x == " ", s))


def set_slide_title(textFrame, titleText):
    # add_formatted_text_runs(textFrame.paragraphs[0], titleText, title_font)
    textFrame.paragraphs[0].text = titleText


def add_formatted_text_runs(para, text, font_size):
    # Track the last position in the text
    last_pos = 0

    # Iterate through patterns and apply formatting
    for match in re.finditer(r"|".join([p[0] for p in patterns]), text):
        start, end = match.span()
        if start > last_pos:
            # Add unformatted text
            run = para.add_run()
            run.text = text[last_pos:start]
            # run.font.size = Pt(font_size)

        # Identify matched formatting
        for pattern, styles in patterns:
            if re.fullmatch(pattern, match.group()):
                run = para.add_run()
                # text_value = next(ftext for ftext in match.groups() if ftext is not None)
                text_value = match.group()
                for ftext in match.groups():
                    if ftext:
                        text_value = ftext
                        break
                run.text = text_value
                for style, value in styles.items():
                    setattr(run.font, style, value)
                break
        last_pos = end

    # Add remaining unformatted text
    if last_pos < len(text):
        run = para.add_run()
        run.text = text[last_pos:]
        run.font.size = Pt(content_font)


def add_slide_content(para, text, indent):
    format_para_for_content(para)

    text = text.strip()
    # bullet_char = ''
    if text.startswith('*') or text.startswith('-'):
        text = text.replace('*', '● ', 1)
        text = text.replace('-', '- ', 1)
        # bullet_char = text[0]
        # text = text.lstrip('-* ')

    # Ensure it's not indented as a bullet
    # Level determines bullet/numbering style (0 is top level)
    para.level = indent

    add_formatted_text_runs(para, text, content_font)

    # TODO: Doesn't work
    # para._element.get_or_add_pPr().set("numId", "1")  # Enable numbering
    # bullet = para._element.get_or_add_pPr().get_or_add_buChar()
    # bullet.set("char", bullet_char)


def create_title_textbox(slide):
    textBox = slide.shapes.add_textbox(Pt(margin), Pt(margin), Pt(textbox_width), Pt(title_height))
    textFrame = textBox.text_frame
    textFrame.word_wrap = True
    textFrame.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
    para = textFrame.paragraphs[0]
    format_para_for_title(para)
    return textFrame


def create_content_textbox(slide, has_title):
    if has_title:
        textBox = slide.shapes.add_textbox(Pt(margin), Pt(content_position), Pt(textbox_width), Pt(content_height_1))
    else:
        textBox = slide.shapes.add_textbox(Pt(margin), Pt(margin), Pt(textbox_width), Pt(content_height_2))

    textFrame = textBox.text_frame
    textFrame.word_wrap = True
    textFrame.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
    return textFrame


def format_para_for_title(para):
    para.line_spacing = font_spacing
    para.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
    para.line_spacing = font_spacing
    para.font.name = font_name
    para.font.size = Pt(title_font)
    para.font.bold = True
    para.font.color.rgb = white_color


def format_para_for_content(para):
    para.line_spacing = font_spacing
    para.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
    para.font.name = font_name
    para.font.size = Pt(content_font)
    para.font.bold = False
    para.font.color.rgb = white_color

    # para.font.bold = True
    # para.font.italic = True
    # para.font.underline = True
    # para.font.strike = True


def set_ppt_spec_for_live():
    global width
    global height
    global margin
    global title_font
    global content_font
    global font_spacing
    global font_name

    # footer only
    width = 1280
    height = 350
    margin = 20

    title_font = 35
    content_font = 26
    font_spacing = 1.1
    font_name = 'Arial'


def set_ppt_spec_for_main():
    global width
    global height
    global margin
    global title_font
    global content_font
    global font_spacing
    global font_name

    # 4:3 ratio
    width = 1440
    height = 1080
    margin = 20

    title_font = 40
    content_font = 34
    font_spacing = 1.2
    font_name = 'Arial'


def convert_text_to_presentation(slides, name):
    # Create presentation
    presentation = create_presentation(width, height)

    # Add slides to presentation
    for slide_content in slides:
        slide = new_slide(presentation)
        has_title = is_title(slide_content[0])
        title_textFrame = create_title_textbox(slide)
        content_textFrame = create_content_textbox(slide, has_title)
        first_content_line = True

        for line in slide_content:
            if is_title(line):
                titleText = line.strip('# ')
                set_slide_title(title_textFrame, titleText)
            elif first_content_line:
                first_content_line = False
                indent = get_indent(line)
                content_para = content_textFrame.paragraphs[0]
                add_slide_content(content_para, line.strip(), indent)
            else:
                indent = get_indent(line)
                content_para = content_textFrame.add_paragraph()
                add_slide_content(content_para, line.strip(), indent)

    presentation.save(name)


def get_slides_list_from_text(filename):
    with open(filename, 'r') as contentfile:
        content = contentfile.readlines()

    # Read ppt content into a slide list
    slides = []
    slide = []
    for line in content:
        line = line.rstrip('\n')
        if line == '==':
            # end of slide, create new slide
            slides.append(slide)
            slide = []
            continue
        slide.append(line)

    # Debug slide list
    print(slides)
    return slides


def main():
    slides = get_slides_list_from_text('content.txt')

    set_ppt_spec_for_main()
    convert_text_to_presentation(slides, 'Presentation Main.pptx')

    set_ppt_spec_for_live()
    convert_text_to_presentation(slides, 'Presentation LIVE.pptx')


if __name__ == "__main__":
    main()
