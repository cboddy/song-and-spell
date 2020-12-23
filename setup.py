#!/usr/bin/env python3
from setuptools import find_packages, setup

def get_long_description():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='song-and-spell',
    version='0.2.0',
    packages=find_packages(),
    author='Chris Boddy',
    author_email='chris@boddy.im',
    url='https://github.com/cboddy/song-and-spell',
    description='A configurable, mutable toddler radio that encourages spelling',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    install_requires=[
        'appdirs==1.4.4',
        'backcall==0.2.0',
        'black==20.8b1',
        'click==7.1.2',
        'dataclasses==0.8',
        'decorator==4.4.2',
        'evdev==1.3.0',
        'Flask==1.1.2',
        'ipython==7.16.1',
        'ipython-genutils==0.2.0',
        'itsdangerous==1.1.0',
        'jedi==0.17.2',
        'Jinja2==2.11.2',
        'MarkupSafe==1.1.1',
        'mypy-extensions==0.4.3',
        'parso==0.7.1',
        'pathspec==0.8.1',
        'pexpect==4.8.0',
        'pickleshare==0.7.5',
        #'pkg-resources==0.0.0',
        'prompt-toolkit==3.0.8',
        'ptyprocess==0.6.0',
        'Pygments==2.7.3',
        'pynput==1.7.1',
        'python-xlib==0.29',
        'regex==2020.11.13',
        'six==1.15.0',
        'toml==0.10.2',
        'traitlets==4.3.3',
        'typed-ast==1.4.1',
        'typing-extensions==3.7.4.3',
        'wcwidth==0.2.5',
        'Werkzeug==1.0.1',
        'wheel',
        'xdg==5.0.1',
        'youtube-dl==2020.12.14',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': ['song_and_spell = app:main'],
    },
)

