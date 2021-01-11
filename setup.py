#!/usr/bin/env python3
from setuptools import find_packages, setup

def get_long_description():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='song-and-spell',
    version='0.20.0',
    packages=find_packages(),
    author='Chris Boddy',
    author_email='chris@boddy.im',
    zip_safe=False,
    url='https://github.com/cboddy/song-and-spell',
    description='A configurable, mutable toddler radio that encourages spelling',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    #data_files=['static/templates', (b ],
    install_requires=[
        'appdirs',
        'backcall',
        'black',
        'click',
        'dataclasses',
        'decorator',
        'evdev',
        'Flask',
        'ipython',
        'ipython-genutils',
        'itsdangerous',
        'jedi',
        'Jinja2',
        'MarkupSafe',
        'mypy-extensions',
        'parso',
        'pathspec',
        'pexpect',
        'pickleshare',
        #'pkg-resources',
        'prompt-toolkit',
        'ptyprocess',
        'Pygments',
        'pynput',
        'python-xlib',
        'regex',
        'six',
        'toml',
        'traitlets',
        'typed-ast',
        'typing-extensions',
        'wcwidth',
        'Werkzeug',
        'wheel',
        'xdg',
        'youtube-dl',
    ],
    include_package_data=True,
    package_data={
        "song_and_spell":["static/templates/*.html"],
    },
    entry_points={
        'console_scripts': ['song_and_spell = song_and_spell.app:main'],
    },
)

