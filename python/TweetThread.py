import geocoder
import threading
import requests
from TweetObj import Tweet

#The point of this class is to make geocoder calls for tweet locations in a separate thread from the main in order to make location.py more efficient
class TweetThread(threading.Thread):
    def __init__(self, tweetList):
        threading.Thread.__init__(self)
        self.tweetList = tweetList
        self.done = False
        self.running = False

    def run(self):
        self.running = True
        i = 1
        for tweet in self.tweetList:
            tweet.coordinates = str(geocoder.arcgis(tweet.location).latlng)
            print("\n\n\n\n*********" + str(i) + "\\" + str(len(self.tweetList)) + "//////////" + tweet.file_name + ": " + tweet.coordinates + "*********\n\n\n\n\n")
            i += 1
        self.done = True
