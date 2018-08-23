from setuptools import setup

setup(name='TwitterNLP',
      version='0.1',
      author='Jake Crawford',
      description='The package for the python Twitter project',
      py_modules=['location','TweetObj','TweetThread','twitterTests'],
      install_requires=['spacy','redis','geocoder',],
      )
