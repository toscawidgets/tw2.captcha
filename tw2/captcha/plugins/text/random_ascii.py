import random
from tw2.captcha.widgets import Captcha

valid_chars = Captcha.ascii_char
num_chars = Captcha.num_char

def generate_text():
    "Generate a random string to display as the captcha text."
    s = []
    for i in range(num_chars):
        s.append(random.choice(valid_chars))
    return ''.join(s)
