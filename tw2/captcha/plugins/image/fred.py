import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

from pkg_resources import resource_filename
from tw2.captcha.widgets import Captcha

# get the font path
font_path = Captcha.text_font_path
assert os.path.exists(font_path), \
       'The font_path "%s" does not exist' % (font_path,)

font_size = Captcha.text_font_size_min

def generate_jpeg(text, file_obj):
    # Settings ----------------------------------------------------
    rand = random.randint
    charNum = len(text)
    charimg_w = font_size + 8
    charimg_h = font_size + 8
    img_w = (font_size * charNum) + 8
    img_h = int(charimg_h * 1.5)
    interval = font_size
    lineNum = rand(5, 15)
    font = ImageFont.truetype(font_path, font_size)

    # Create a background -----------------------------------------
    bg_color = rand(0xbb, 0xee)
    image = Image.new('RGB', (img_w, img_h), (bg_color, bg_color, bg_color))

    # Generate text -----------------------------------------------
    for i in range(0, charNum):
        color = rand(0x111111, 0x444444)
	# Create a small image to hold one character. Background is black
	charImg = Image.new('RGB', (charimg_w, charimg_h), 0)
	tmpDraw = ImageDraw.Draw(charImg)
	# Draw text on this image
	tmpDraw.text((3, 1), text[i], font=font, fill=color)
	# Rotate a little bit, do some trick if you want
	charImg = charImg.rotate(rand(-20,20))

	# Create a mask which is same size of the small image
	mask = Image.new('L', (charimg_w, charimg_h), 0)
	mask.paste(charImg, (0, 0))

	# Generate Random X Y
	hpos = 8 + (i * interval) + rand(-8, 5)
	vpos = rand(5, 15)

	image.paste(charImg, (hpos, vpos), mask)
	image.paste(charImg, (hpos+1, vpos+1), mask)

    image = image.filter(ImageFilter.SHARPEN)

    # Draw few lines -----------------------------------------
    draw = ImageDraw.Draw(image)
    for i in range(0, lineNum):
        draw.line((rand(1, img_w), rand(1, img_h),
                   rand(1, img_w), rand(1, img_h)),
                  fill=rand(0x666666, 0x999999)
                  )

    image.save(file_obj, format='JPEG')

if __name__ == "__main__":
    generate_jpeg('hello', '/tmp/foo.jpg')
    print "Captcha image generated."
