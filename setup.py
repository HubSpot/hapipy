#!/usr/bin/env python
from distutils.core import setup

setup(
    name='hapipy',
    version='2.1.4',
    description="A python wrapper around HubSpot's APIs",
    author='Adrian Mott',
    author_email='amott@hubspot.com',
    url='https://github.com/HubSpot/hapipy',
    download_url='https://github.com/HubSpot/hapipy/tarball/v2.1.4',
    packages=['hapi'],
    install_requires=[
        'nose==1.1.2',
        'unittest2==0.5.1',
        'simplejson==2.2.1'
    ],
    long_description = """
        Full docs at: https://github.com/HubSpot/hapipy
    """
)
