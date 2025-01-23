from PIL import Image, ImageDraw, ImageFont
import os

from presentations.create_ppt_from_text import black_color, is_title

img_format = 'png'
img_width = 1900
img_height = 300
margin = 20
img_offset2 = (img_width / 2) + margin
img_font_spacing = 15

font_arial = '/System/Library/Fonts/Supplemental/Arial.ttf'
font_telugu = '/System/Library/Fonts/KohinoorTelugu.ttc'


def init_images_dir(dir):
    # Clear older images
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def create_lyrics_images(content, dir):
    for img_name, text1, text2 in content:
        image = Image.new(mode="RGB", size=(img_width, img_height), color=black_color)
        imageDraw = ImageDraw.Draw(image)

        if text2:
            # Telugu (to the left)
            img_font = ImageFont.truetype(font_telugu, size=40)
            imageDraw.multiline_text(xy=(margin, margin), font=img_font, spacing=img_font_spacing, text=text1)
        else:
            # English only (centered)
            img_font = ImageFont.truetype(font_arial, size=44)

            # textbbox returns: left, top, right, bottom
            bbox = imageDraw.textbbox(xy=(0, 0), font=img_font, spacing=img_font_spacing, text=text1)
            margin_left = (img_width - bbox[2]) / 2
            imageDraw.multiline_text(xy=(margin_left, margin), font=img_font, spacing=img_font_spacing, text=text1)

        if text2:
            # English (to the right)
            img_font = ImageFont.truetype(font_arial, size=44)
            imageDraw.multiline_text(xy=(img_offset2, margin), font=img_font, spacing=img_font_spacing,
                                     text=text2)

        image.save(fp=os.path.join(dir, img_name))

    return


def create_ppt_images(slides, spec, dir):
    image_counter = 0

    for slide_content in slides:
        image = Image.new(mode="RGB", size=(spec.width, spec.height), color=black_color)
        imageDraw = ImageDraw.Draw(image)
        image_counter = image_counter + 1
        content_position = spec.margin_top
        if is_title(slide_content[0]):
            titleText = slide_content[0].strip('# ')
            img_font = ImageFont.truetype(spec.font_name, size=spec.title_font)
            imageDraw.text(xy=(spec.margin_left, spec.margin_top), font=img_font, spacing=spec.font_spacing,
                           text=titleText)
            slide_content = slide_content[1:]
            content_position = spec.content_position

        contentText = '\n'.join(slide_content)
        contentText = contentText.replace('_', '').replace('*', '')
        img_font = ImageFont.truetype(spec.font_name, size=spec.content_font)
        imageDraw.text(xy=(spec.margin_left, content_position), font=img_font, spacing=spec.font_spacing,
                       text=contentText)

        image.save(fp=os.path.join(dir, f'ICC Message {image_counter:02.0f}.png'))

    return
