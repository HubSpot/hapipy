#!/usr/bin/env python
from distutils.core import setup

setup(
    name='hapipy',
    version='dev',
    description='Python HubSpot Api Wrapper',
    author='Adrian Mott',
    author_email='adrianmott@gmail.com',
    url='',
    packages=['hapi'],
    install_requires=[
        'nose==1.1.2',
        'unittest2==0.5.1',
    ]
)
