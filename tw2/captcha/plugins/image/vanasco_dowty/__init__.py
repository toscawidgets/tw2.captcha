import captcha
import random
import os.path
from pkg_resources import resource_filename
from tw2.captcha.widgets import Captcha

width = Captcha.picture_width
height = Captcha.picture_height
bg_color = Captcha.picture_bg_color
fg_color = Captcha.picture_fg_color
font_size_min = Captcha.text_font_size_min
font_size_max = Captcha.text_font_size_max

captcha.font__paths = [Captcha.text_font_path]
for font_path in captcha.font__paths:
    assert os.path.exists(font_path), \
            'The font_path "%s" does not exist' % (font_path,)
captcha.captcha__text__render_mode = Captcha.text_render_mode
captcha.captcha__font_range = (font_size_min, font_size_max)


def generate_jpeg(text, file_):
    font_size = random.randint(font_size_min, font_size_max)
    fg = random.choice(fg_color)
    ci = captcha._Captcha__Img(text, width, height, font_size, fg, bg_color)
    image = ci.render()
    image.save(file_, format='JPEG')
