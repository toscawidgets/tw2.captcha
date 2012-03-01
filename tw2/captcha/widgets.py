"""
tw2 widgets that provides text or audio captcha.
"""

import tw2.core as twc

import base64
import model
import os
import random
from Crypto.Cipher import AES
from cStringIO import StringIO
from sha import new as sha_constructor
from pkg_resources import iter_entry_points

modname = '.'.join(__name__.split('.')[:-1])

class CaptchaWidget(twc.Widget):
    template = "mako:tw2.captcha.templates.captcha"


class Captcha(CaptchaWidget):
    resources = CaptchaWidget.resources + [
        twc.CSSLink(modname=modname, filename="static/ext/captcha.css"),
    ]

    key = twc.Param(
        "Random string unique for your site with which the captcha is generated.",
        default=None)
    audio = twc.Param("Boolean to enable or not audio captcha.",
        default=True)
    jpeg_generator = twc.Param(
        "Algorithm used to render the captcha image. Options:vanasco_dowty, mcdermott",
        default='vanasco_dowty')
    text_generator = twc.Param("Text displayed on the captcha image.",
        default='random_ascii')
    timeout = twc.Param("Time in minutes during which the captcha will be valid.",
        default=5)

    picture_width = twc.Param("Picture width in pixel.", default=300)
    picture_height = twc.Param("Picture width in pixel.", default=100)
    picture_bg_color = twc.Param('Picture background color.', default='#DDDDDD')
    picture_fg_color = twc.Param('Picture foreground color.',
        default= ["#330000","#660000","#003300","#006600","#000033","#000066"])
    text_font_size_min = twc.Param(
        'Minimal font size for the text on the captcha.', default=30)
    text_font_size_max = twc.Param(
        'Maximal font size for the text on the captcha.', default=45)
    text_font_path = twc.Param('Full path to the font to be used in for the text.',
        default= 'tw2/captcha/static/fonts/tuffy/Tuffy.ttf')
    text_render_mode = twc.Param('Rendering method for the text.', 
        default='by_letter')
    ascii_char = twc.Param('Character allowed in the ascii text',
        default='BCDEFGHJKLMNPQRTUVWXYacdefhijkmnprstuvwxyz378')
    num_char = twc.Param('Number of character to put on the captcha',
        default=5)
    start_range = twc.Param('For the equation, minimum number allowed',
        default=1)
    stop_range = twc.Param('For the equation, maximum number allowed',
        default=100)


    def prepare(self):

        # Check the types of everything
        if self.key == None:
            raise ValueError("Captcha must be provided a `key` parameter")
        if self.jpeg_generator == None:
            raise ValueError("Captcha must have a jpeg_generator")
        if self.text_generator == None:
            raise ValueError("Captcha must have a text_generator")
        int(self.start_range)
        int(self.stop_range)
        int(self.num_char)
        int(self.timeout)
        int(self.picture_width)
        int(self.picture_height)
        int(self.text_font_size_max)
        int(self.text_font_size_min)
        print self.key

        self.key = sha_constructor(self.key).hexdigest()[:32]
        random.seed()
        self.aes = AES.new(self.key, AES.MODE_ECB)
        # find the jpeg generator
        jpeg_gen = self.jpeg_generator
        print "**", self.jpeg_generator, self.text_generator, self.key
        for ep in iter_entry_points('tw2.captcha.jpeg_generators', jpeg_gen):
            self.jpeg_generator = ep.load()
        # find the text generator
        txt_gen = self.text_generator
        for ep in iter_entry_points('tw2.captcha.text_generators', txt_gen):
            self.text_generator = ep.load()

        payload = self.create_payload()
        print "********************", payload
        image = self.image(payload)

    def image(self, value):
        "Serve a jpeg for the given payload value."
        scp = self.model_from_payload(value)
        f = StringIO()
        if scp.label is not None and scp.label != None:
            self.jpeg_generator(scp.label, f)
        else:
            self.jpeg_generator(scp.plaintext, f)
        f.seek(0)
        return f.read()

    def create_payload(self):
        "Create a payload that uniquely identifies the captcha."
        c = model.Captcha()
        c.plaintext = self.text_generator()
        if isinstance(c.plaintext, tuple):
             c.label = "%i + %i =" % (c.plaintext[0], c.plaintext[1])
             c.plaintext = str(c.plaintext[0] + c.plaintext[1])
        s = c.serialize()
        # pad shortfall with multiple Xs
        if len(s) % 16:
            pad = (16 - (len(s) % 16)) * 'X'
            s = "".join((s, pad))
        enc = self.aes.encrypt(s)
        return base64.urlsafe_b64encode(enc)

    def model_from_payload(self, ascii_payload):
        "Convert a payload to a SCPayload object."
        enc = base64.urlsafe_b64decode(ascii_payload)
        s = self.aes.decrypt(enc)
        s = s.rstrip('X')
        return model.Captcha.deserialize(s)
