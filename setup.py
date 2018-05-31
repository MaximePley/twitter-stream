# -*- coding: utf-8 -*-

from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='twitter-listener',
    version='0.1dev',
    description='Filter Twitter stream and send follower requests',
    long_description=readme,
    author='Maxime Pley',
    author_email='pleymaxime@gmail.com',
    url='https://github.com/MaximePley/twitter-stream'
)
