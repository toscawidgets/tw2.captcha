"""
tw2 widgets that provides text or audio captcha.
"""

import tw2.core as twc
import tw2.forms as twf

import base64
import model
import os
import random
import subprocess as sp  # omg
import tempfile
import urllib2
import webob

from Crypto.Cipher import AES
from cStringIO import StringIO
from sha import new as sha_constructor
from pkg_resources import iter_entry_points

from tw2.captcha.validators import CaptchaValidator

modname = '.'.join(__name__.split('.')[:-1])

captcha_css = twc.CSSLink(modname=modname, filename="static/ext/captcha.css")
captcha_img = twc.DirLink(modname=modname, filename="static/images/")

class Captcha(twf.TextField):
    template = "mako:tw2.captcha.templates.captcha"
    resources = [captcha_css, captcha_img]

    key = twc.Param(
        "Random string unique for your site with which the captcha is generated.",
        default="CHANGEME")
    _key = twc.Variable("Used internally.")

    audio = twc.Param("Boolean to enable or not audio captcha.",
        default=True)
    audio_icon = twc.Param(
        "URL for an audio icon.",
        default="/resources/tw2.captcha/static/images/gnome_audio_volume_medium.png",
    )

    jpeg_generator = twc.Param(
        "Algorithm used to render the captcha image.  " +
        "Options:vanasco_dowty, mcdermott",
        default='vanasco_dowty')
    text_generator = twc.Param(
        "Text displayed on the captcha image.",
        default='random_ascii')
    timeout = twc.Param(
        "Time in minutes during which the captcha will be valid.",
        default=5)

    controller_prefix = twc.Param("URL prefix of captcha controller",
                                  default="__tw2_captcha__")
    picture_width = twc.Param("Picture width in pixel.", default=300)
    picture_height = twc.Param("Picture width in pixel.", default=100)
    picture_bg_color = twc.Param('Picture background color.', default='#DDDDDD')
    picture_fg_color = twc.Param('Picture foreground color.',
        default= ["#330000","#660000","#003300","#006600","#000033","#000066"])
    text_font_size_min = twc.Param(
        'Minimal font size for the text on the captcha.', default=30)
    text_font_size_max = twc.Param(
        'Maximal font size for the text on the captcha.', default=45)
    text_font_path = twc.Param(
        'Full path to the font to be used in for the text.  ' +
        'Either relative to the package or absolute.',
        default='static/fonts/tuffy/Tuffy.ttf')
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

    payload = twc.Variable("Internally used hash of the captcha.")

    @classmethod
    def post_define(cls):
        # Modify the text_font_path, allowing either relative or absolutely
        # pathed font paths.
        if not cls.text_font_path[0] == os.path.sep:
            base = os.path.sep.join(__file__.split(os.path.sep)[:-1])
            cls.text_font_path = base + os.path.sep + cls.text_font_path

        # Check the types of everything
        if cls.key == None:
            raise ValueError("Captcha must be provided a `key` parameter")
        if cls.jpeg_generator == None:
            raise ValueError("Captcha must have a jpeg_generator")

        # Set up our key and aes.
        cls._key = sha_constructor(cls.key).hexdigest()[:32]
        random.seed()
        cls.aes = AES.new(cls._key, AES.MODE_ECB)

        # Set up our validator with a reference back to us.
        cls.validator = CaptchaValidator(captcha_widget=cls)

    @classmethod
    def load_jpeg_generator(cls):
        name = cls.jpeg_generator
        for ep in iter_entry_points('tw2.captcha.jpeg_generators', name):
            return ep.load()

    @classmethod
    def request(cls, req):
        """ When a widget is first served, :meth:`prepare` and :meth:`display`
        are called which produce the HTML embedded on the page - the captcha.

        That embedding produces one or more subsequent requests for the actual
        image (and potentially some audio).  Those requests make their way here.
        """

        nothing, prefix, directive, payload = req.path.split('/')
        assert(prefix == cls.controller_prefix)

        payload = urllib2.unquote(payload)
        scp = cls.model_from_payload(payload)

        sub_controllers = {
            'image': cls.request_image,
            'audio': cls.request_audio,
        }
        stream, content_type = sub_controllers[directive](scp)
        resp = webob.Response(app_iter=stream, content_type=content_type)
        return resp

    @classmethod
    def request_audio(cls, scp):
        """ Returns raw binary audio and the content type """

        # FIXME -- how dangerous is this, running Popen from a webapp?

        fd, filename = tempfile.mkstemp('.wav')
        try:
            cmd = ['espeak', '%s' % scp.label, '-w', '%s' % filename]
            proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
            output, error = proc.communicate()
        except Exception, err:
            print "ERROR: %s" % err

        f = open(filename)
        f.seek(0)
        content = f.read()
        os.remove(filename)
        return content, 'audio/basic'

    @classmethod
    def request_image(cls, scp):
        """ Returns a raw binary image and the content type """
        f = StringIO()
        if scp.label is not None and scp.label != None:
            cls.load_jpeg_generator()(scp.label, f)
        else:
            cls.load_jpeg_generator()(scp.plaintext, f)
        f.seek(0)
        res = f.read()
        return res, 'image/jpeg'

    @classmethod
    def model_from_payload(cls, ascii_payload):
        """ Convert a payload to a SCPayload object. """
        enc = base64.urlsafe_b64decode(ascii_payload)
        s = cls.aes.decrypt(enc)
        s = s.rstrip('X')
        return model.Captcha.deserialize(s)

    def prepare(self):
        """ Called just before the widget is displayed. """
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

        # find the text generator
        txt_gen = self.text_generator
        for ep in iter_entry_points('tw2.captcha.text_generators', txt_gen):
            self.text_generator = ep.load()

        self.payload = self.create_payload()

        # Register our widget's built-in controller with the middleware
        # This allows subsequent requests (for the image and the audio) to make
        # their way to this widget's `request` method.
        mw = twc.core.request_local()['middleware']
        mw.controllers.register(type(self), self.controller_prefix)

        super(Captcha, self).prepare()

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
        enc = type(self).aes.encrypt(s)
        return base64.urlsafe_b64encode(enc)
