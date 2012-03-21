from setuptools import setup, find_packages

f = open('README.rst')
long_description = f.read().strip()
long_description = long_description.split('split here', 1)[1]
f.close()

install_requires=[
    "tw2.core",
    "pycrypto",
    "PIL",
    "kitchen",
]

import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    install_requires.extend([
        "ordereddict",
    ])

setup(
    name='tw2.captcha',
    version='0.0.4',
    description='toscawidgets2 captcha plugin',
    long_description=long_description,
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    url='http://github.com/toscawidgets/tw2.captcha',
    install_requires=install_requires,
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages = ['tw2'],
    zip_safe=False,
    include_package_data=True,
    entry_points="""
        [tw2.widgets]
            # Register your widgets so they can be listed in the WidgetBrowser
            tw2.captcha = tw2.captcha
        [tw2.captcha.jpeg_generators]
            mcdermott = tw2.captcha.plugins.image.mcdermott:generate_jpeg
            vanasco_dowty = tw2.captcha.plugins.image.vanasco_dowty:generate_jpeg
            fred = tw2.captcha.plugins.image.fred:generate_jpeg
        [tw2.captcha.text_generators]
            random_ascii = tw2.captcha.plugins.text.random_ascii:generate_text
            random_equation = tw2.captcha.plugins.text.random_equation:generate_text
            fivelettername = tw2.captcha.plugins.text.fivelettername:generate_text
    """,
    keywords = [
        'toscawidgets.widgets',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
