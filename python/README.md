# Python Scripts
---

There are a few Python scripts in this folder that do a variety of things

1. location: This is the main script for the Twitter project. It does all the natural language 
processing and it's where most of everything is done

2. redistest: This script is just a simple test for Redis and a few other various things

3. TweetObj: This script is just an Object representation of the important information for tweets

4. TweetThread: This script allows location.py to be a threaded program. Due to this file the
geocoder calls can be done in separate threads from the NLP.
