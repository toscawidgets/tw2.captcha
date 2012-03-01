import random
from tw2.captcha.widgets import Captcha

range_start = Captcha.start_range
range_end = Captcha.stop_range

def generate_text():
    "Generate two random numbers to display as the captcha text."
    first = random.randint(range_start, range_end)
    second = random.randint(range_start, range_end)
    return (first, second)
