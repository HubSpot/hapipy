#!/usr/bin/env python
from setuptools import setup

setup(
    name='hapipy',
    version='2.10.5',
    description="A python wrapper around HubSpot's APIs",
    long_description=open('README.md').read(),
    author='HubSpot Dev Team',
    author_email='devteam+hapi@hubspot.com',
    url='https://github.com/HubSpot/hapipy',
    download_url='https://github.com/HubSpot/hapipy/tarball/v2.10.5',
    license='LICENSE.txt',
    packages=['hapi', 'hapi.mixins'],
    install_requires=[
        'simplejson>=2.1.2'
    ],
)
