from distutils.core import setup

setup(name='TwitterNLP',
      version='1.0',
      author='Jake Crawford',
      description='The package for the python Twitter project',
      py_modules=['location','TweetObj','TweetThread','twitterTests'],
      install_requires=['spacy','redis','geocoder','pickle'],
      )
