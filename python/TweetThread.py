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
            print("\n\n\n\n*********" + str(len(self.tweetList)) + "//////////" + tweet.file_name + ": " + tweet.coordinates + "*********\n\n\n\n\n")
        self.done = True

'''
tlist = [Tweet("json_text", "Virginia", "testfile.txt")]
thread = TweetThread(tlist)
thread.start()
while(not thread.done):
    print("waiting")
print(thread.tweetList[0].coordinates, str(thread.tweetList[0]))
'''
