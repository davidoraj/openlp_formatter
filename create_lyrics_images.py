from PIL import Image, ImageDraw, ImageFont
import os

# Image / PPT Creation
dir = 'images'

img_format = 'png'
img_offset_top = 20
img_offset1 = 20
img_offset2 = 980
img_font_spacing = 15
img_font = ImageFont.truetype('Nirmala.ttf', size=44)
img_width = 1920
img_height = 350


def init_images_dir():
    # Clear older images
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def save_to_images(content):
    for img_name, text1, text2 in content:
        image = Image.new(mode="RGB", size=(img_width, img_height), color=(0, 200, 0))
        imageDraw = ImageDraw.Draw(image)
        imageDraw.multiline_text(xy=(img_offset1, img_offset_top), font=img_font, spacing=img_font_spacing, text=text1)
        if text2:
            imageDraw.multiline_text(xy=(img_offset2, img_offset_top), font=img_font, spacing=img_font_spacing,
                                     text=text2)
        image.save(fp=os.path.join(dir, img_name))

    return
