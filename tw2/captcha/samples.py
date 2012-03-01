""" Samples of how to use tw2.captcha

Each class exposed in the widgets submodule has an accompanying Demo<class>
widget here with some parameters filled out.

The demos implemented here are what is displayed in the tw2.devtools
WidgetBrowser.
"""

from widgets import (
    Captcha,
)


class DemoCaptcha(Captcha):
    key = "lkdsfhaldskflkfdalkfkahg;ahupiuyghi"
    audio = True

    jpeg_generator = 'vanasco_dowty'
    text_generator = 'random_equation'

