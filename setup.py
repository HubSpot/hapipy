#!/usr/bin/env python
from setuptools import setup

setup(
    name='hapipy',
    version='2.10.5.4+bs2',
    description="A python wrapper around HubSpot's APIs",
    long_description=open('README.md').read(),
    author='HubSpot Dev Team',
    author_email='devteam+hapi@hubspot.com',
    url='https://github.com/HubSpot/hapipy',
    download_url='https://github.com/HubSpot/hapipy/tarball/v2.10.3',
    license='LICENSE.txt',
    packages=['hapi', 'hapi.mixins'],
    install_requires=[
        'simplejson>=2.1.2',
        'six>=1.12.0',
        'future>=0.18.2'
    ],
)
