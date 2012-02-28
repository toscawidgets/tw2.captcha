tw2.captcha
===========

:Author: Pierre-Yves Chibon <pingou@pingoured.fr>

.. comment: split here

.. _toscawidgets2 (tw2): http://toscawidgets.org/documentation/tw2.core/

tw2.captcha is a `toscawidgets2 (tw2)`_ captcha plugin

Live Demo
---------

Peep the `live demonstration <http://tw2-demos.threebean.org/module?module=tw2.captcha>`_.

Links
-----

You can `get the source from github <http://github.com/pypingou/tw2.captcha>`_,
report or look into `bugs <http://github.com/pypingou/tw2.captcha/issues/>`_.

Description
-----------

`toscawidgets2 (tw2)`_ aims to be a practical and useful widgets framework
that helps people build interactive websites with compelling features, faster
and easier. Widgets are re-usable web components that can include a template,
server-side code and JavaScripts/CSS resources. The library aims to be:
flexible, reliable, documented, performant, and as simple as possible.

This module, tw2.captcha, provides `toscawidgets2 (tw2)`_ a  captcha widget.


Sampling tw2.captcha in the WidgetBrowser
------------------------------------

The best way to scope out ``tw2.captcha`` is to load its widgets in the
``tw2.devtools`` WidgetBrowser.  To see the source code that configures them,
check out ``tw2.captcha/tw2/captcha/samples.py``

To give it a try you'll need git, mercurial, python, and virtualenv.  Run::

    $ git clone git://github.com/pypingou/tw2.captcha.git
    $ cd tw2.captcha
    $ mkvirtualenv tw2.captcha
    (tw2.captcha) $ pip install tw2.devtools
    (tw2.captcha) $ python setup.py develop
    (tw2.captcha) $ paster tw2.browser

...and browse to http://localhost:8000/ to check it out.



