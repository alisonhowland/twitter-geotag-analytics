import geocoder
import threading
import requests
from TweetObj import Tweet

class TweetThread(threading.Thread):
    def __init__(self, tweetList):
        self.tweetList = tweetList

    def run(self):
        with requests.Session() as session:
            for tweet in self.tweetList:
                tweet.coordinates = geocoder.arcgis(tweet.location, session=session).latlng

tlist = [Tweet("json_text", "Virginia", "testfile.txt")]
thread = TweetThread(tlist)
thread.run()
print(thread.tweetList[0].coordinates)
