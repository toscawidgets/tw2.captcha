import random
import Image
import ImageFont
import ImageDraw
import ImageFilter
from pkg_resources import resource_filename
import os.path
from tw2.captcha.widgets import Captcha

# get the font path
font_path = Captcha.text_font_path
assert os.path.exists(font_path), \
        'The font_path "%s" does not exist' % (font_path,)

text_font_size_min = Captcha.text_font_size_min
bgcolor = Captcha.picture_bg_color
fgcolor = Captcha.picture_fg_color
# Code taken from
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440588
# written by Robert McDermott

def generate_jpeg(text, file_obj):
    """Generate a captcha image"""
    # randomly select the foreground color
    fgcolor = random.randint(0,0xffff00)
    # make the background color the opposite of fgcolor
    bgcolor = fgcolor ^ 0xffffff
    # create a font object
    font = ImageFont.truetype(font_path, text_font_size_min)
    # determine dimensions of the text
    dim = font.getsize(text)
    # create a new image slightly larger that the text
    im = Image.new('RGB', (dim[0]+5,dim[1]+5), bgcolor)
    d = ImageDraw.Draw(im)
    x, y = im.size
    r = random.randint
    # draw 100 random colored boxes on the background
    for num in range(100):
        d.rectangle((r(0,x),r(0,y),r(0,x),r(0,y)),fill=r(0, bgcolor ^ 0xffffff))
    # add the text to the image
    d.text((3,3), text, font=font, fill=fgcolor)
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # save the image to a file
    im.save(file_obj, format='JPEG')
