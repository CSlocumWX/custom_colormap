# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='custom_colormaps',
    version='2.0',
    description='A small routine to generate custom colormaps for Matplotlib',
    long_description=readme,
    author='Chris Slocum',
    author_email='Christopher.Slocum@colostate.edu',
    url='https://github.com/CSlocumWX/custom_colormap',
    license=license,
    packages=find_packages(exclude=('test', 'docs'))
)
