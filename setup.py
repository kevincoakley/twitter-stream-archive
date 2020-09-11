#!/usr/bin/env python

try:
    from setuptools import setup
    extra = dict(install_requires=[
        'prometheus-client>=0.7.1',
        'tweepy>=3.8.0',
    ],
        include_package_data=True,
        test_suite="tests.suite.load_tests",
    )
except ImportError:
    from distutils.core import setup
    extra = {}


def readme():
    with open("README.md") as f:
        return f.read()


setup(name="twitter-stream-archive",
      version="1.0.0",
      description="",
      long_description=readme(),
      author="Kevin Coakley",
      author_email="kcoakley@sdsc.edu",
      scripts=[
          "bin/twitter-stream-archive",
      ],
      url="",
      packages=[
          "twitterstreamarchive",
      ],
      platforms="Posix; MacOS X",
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
      ],
      **extra
      )
