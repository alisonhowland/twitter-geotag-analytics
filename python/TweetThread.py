import geocoder
import threading
import requests
from TweetObj import Tweet


class TweetThread(threading.Thread):
    def __init__(self, tweetList):
        threading.Thread.__init__(self)
        self.tweetList = tweetList
        self.done = False
        self.running = False

    def run(self):
        self.running = True
        for tweet in self.tweetList:
            tweet.coordinates = str(geocoder.arcgis(tweet.location).latlng)
            self.done = True

'''
tlist = [Tweet("json_text", "Virginia", "testfile.txt")]
thread = TweetThread(tlist)
thread.start()
while(not thread.done):
    print("waiting")
print(thread.tweetList[0].coordinates)
'''
