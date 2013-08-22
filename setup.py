#!/usr/bin/env python

from setuptools import setup

long_desc = open('readme.rst').read()

setup(name = 'montyhall',
      version = '0.5.3',
      py_modules = ['montyhall'],
      author = 'Morrolan',
      author_email = 'morrolan@icloud.com',
      url = 'http://morrolan.github.io/montyhall/',
      license = 'GNU General Public License (GPL)',
      description = 'Monty Hall Problem Solver.',
      long_description = long_desc,
      platforms = ['Windows','Unix','OS X'],
      download_url = "https://pypi.python.org/pypi/montyhall/",
      keywords = ["surreal", "surrealism", "error message"],
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
         ],
      install_requires=['setuptools'],
      
      )
