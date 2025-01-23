from PIL import Image, ImageDraw, ImageFont
import os

img_format = 'png'
img_width = 1900
img_height = 300
margin = 20
img_offset2 = (img_width / 2) + margin
img_font_spacing = 15
# img_font = ImageFont.truetype('Nirmala.ttf', size=44)

font_arial = '/System/Library/Fonts/Supplemental/Arial.ttf'
font_telugu = '/System/Library/Fonts/KohinoorTelugu.ttc'


def init_images_dir(dir):
    # Clear older images
    for f in os.listdir(dir):
        print(f'deleting {os.path.join(dir, f)}')
        # os.remove(os.path.join(dir, f))


def create_lyrics_images(content, dir):
    for img_name, text1, text2 in content:
        image = Image.new(mode="RGB", size=(img_width, img_height), color=(0, 200, 0))
        imageDraw = ImageDraw.Draw(image)

        if text2:
            img_font = ImageFont.truetype(font_telugu, size=40)
        else:
            img_font = ImageFont.truetype(font_arial, size=44)
        imageDraw.multiline_text(xy=(margin, margin), font=img_font, spacing=img_font_spacing, text=text1)

        if text2:
            img_font = ImageFont.truetype(font_arial, size=44)
            imageDraw.multiline_text(xy=(img_offset2, margin), font=img_font, spacing=img_font_spacing,
                                     text=text2)

        image.save(fp=os.path.join(dir, img_name))

    return
