import spacy
import redis
import geocoder
import os
import pickle
from spacy import displacy

READ_PATH = "/var/local/tempTestData/"
WRITE_PATH = "/var/local/data_out/"

#Saves the given dictionary to a file
#DEPRECIATED. USE REDIS FOR SAVING DATA NOW
def save_dictionary(dictionary):
   with open("dictionary.pkl", "wb") as f:
      pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)
      
#Returns the saved dictionary file
#DEPRECIATED. USE REDIS FOR SAVING DATA NOW
def load_dictionary():
   with open("dictionary.pkl", "rb") as f:
      return pickle.load(f)

#Returns True if redis already has the specified key in its database
#Red is the instance of redis; key is the key to check
def redisHasKey(red, key):
   return not(red.get(key) == None)

#Returns a String of the location value in the JSON file
#json_text is the json file in String form. Now more generic!
def getLocation(json_text):
   start1 = json_text.find("user_location")
   start2 = len("user_location") + start1 + 1
   end1 = json_text.find("\"", start2)
   end2 = json_text.find("\"", end1 + 1)
   return json_text[end1 + 1 : end2 - 1]

#Writes the json file with the specified file name to the 'constant' output directory with the
#appropriate coordinates and text. Now more generic!
def writeCoordinates(coordinates, file_name, json_text):
   index = json_text.find("Coordinates")
   index2 = json_text.find("\"", index + len("Coordinates") + 2)
   outString = json_text[: index2 + 1] + str(coordinates) + json_text[index2 + 3 :]
   writer = open(WRITE_PATH + file_name, "w")
   writer.write(outString)
   writer.close()

#Returns True if there is anything in the location tag, and False otherwise
def hasLocation(json_text):
   return len(getLocation(json_text)) >= 1

#Returns a String of the Tweet's text taken from the JSON file
#json_text is the json file in String form. Now more generic!
def getTweet(json_text):
   start1 = json_text.find("tweet_text")
   start2 = len("tweet_text") + start1 + 1
   end1 = json_text.find("\"", start2)
   end2 = json_text.find("\"", end1 + 1)
   return json_text[end1 + 1 : end2 - 1]

#Returns the language code of the JSON file. We probably shouldn't try to parse 
#non-english languages with SpaCy
#DEPRECIATED AS OF THE NEW METADATA MODEL
def getLanguage(json_text):
   index = json_text.find(",\"lang\":")
   index2 = json_text.find(",\"user_description")
   return json_text[index + 9 : index2 - 1]


#'main' method as of now
red = redis.Redis(host='localhost', port=6379, password='')
files = os.listdir(READ_PATH)
for file_name in files:
   json = open(READ_PATH + file_name, "r")
   data = json.read()
   json.close()
   if hasLocation(data):
      location = getLocation(data)
      if redisHasKey(red, location.lower()):
         coordinates = red.get(location)
      else:
         coordinates = geocoder.arcgis(location).latlng
         red.set(location.lower(), str(coordinates))
      print(location, coordinates)
      writeCoordinates(coordinates, file_name, data)
      os.remove(READ_PATH + file_name)
save_dictionary(dictionary)


'''
i = 0
red = redis.Redis(host='localhost', port=6379, password='')
dictionary = load_dictionary()
for key in dictionary:
   print(key, dictionary[key])
   if not(redisHasKey(red, key.lower())):
      red.set(key.lower(), str(dictionary[key]))
   i += 1
print(i)


print(red.get("va"))
print(red.get("tx"))
print(red.get("vermont"))
print(red.dbsize())


reader = open(READ_PATH + "1215309993635823.json")
text = reader.read()
reader.close()
print(getLocation(text), getTweet(text))
writeCoordinates([1,1], "1215309993635823.json", text)
'''
#nlp = spacy.load('en_core_web_lg')
#sample = open("tweet.txt")
#doc = nlp(sample.read())
#sample.close()
#for ent in doc.ents:
#   if ent.label_ == "LOC" or ent.label_ == "GPE":
#      print(ent.text, ent.label_, str(geocoder.arcgis(ent.text).latlng))
