import spacy
import redis
import geocoder
import os
import sys
import pickle
#from spacy import displacy

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
   return json_text[end1 + 1 : end2]

#Writes the json file with the specified file name to the 'constant' output directory with the
#appropriate coordinates and text. Now more generic!
def writeCoordinates(coordinates, file_name, json_text):
   index = json_text.find("Coordinates")
   index2 = json_text.find("\"", index + len("Coordinates") + 2)
   outString = json_text[: index2 + 1] + str(coordinates) + json_text[index2 + 1 :]
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
   return json_text[end1 + 1 : end2]

#Returns True if there is anything in the text tag, and False otherwise
def hasTweet(json_text):
   return len(getTweet(json_text)) >= 1

#Returns a string that is the best location that could be pulled from the tweet
def getTweetLocation(json_text, red, nlp):
   if getLanguage(json_text) != "en": #this program is not eqipped to deal with foriegn languages
      return ""

   if hasTweet(json_text):
      tweet = getTweet(json_text)
   else:
      return ""
   doc = nlp(tweet)
   entities = doc.ents
   numEntities = len(entities)
   bestEntity = ""
   for entity in entities:
      if (entity.label_ == "LOC" or entity.label_ == "GPE") and redisHasKey(red, entity.text.lower()):
         bestEntity = entity.text #Cross-checks redis db to find entity that is most likely to be a place

   if bestEntity == "" and numEntities == 0:
      return ""
   elif bestEntity == "" and numEntities > 0:   
      return entities[numEntities - 1].text
   else:
      return bestEntity

#Returns the language code of the JSON file. We probably shouldn't try to parse 
#non-english languages with SpaCy
def getLanguage(json_text):
   start1 = json_text.find(",\"lang\":")
   start2 = start1 + len(",\"lang\":") + 1
   end = json_text.find("\"", start2)
   return json_text[start2: end]


#'main' method as of now

nlp = spacy.load('en_core_web_lg')
red = redis.Redis(host='localhost', port=6379, password='')
files = os.listdir(READ_PATH)
for file_name in files:
   
   json = open(READ_PATH + file_name, "r")
   data = json.read()
   json.close()
   
   if hasLocation(data): #it goes into this block if there's a location in the location tag
      location = getLocation(data)
   else:
      location = getTweetLocation(data, red, nlp)

   if redisHasKey(red, location.lower()):
      coordinates = red.get(location.lower()).decode('utf-8')
   else:
      coordinates = geocoder.arcgis(location).latlng

   if coordinates != None:
      red.set(location.lower(), str(coordinates))
      print(location, coordinates, file_name)
      writeCoordinates(coordinates, file_name, data)
   os.remove(READ_PATH + file_name)
red.save()


'''
red = redis.Redis(host='localhost', port=6379, password='')
va = red.get("va").decode('utf-8')
print(va)
print(va[2: (len(va) - 1)])
print(red.get("tx").decode('utf-8'))
print(red.get("vermont"))
print(red.dbsize())
red.save()

reader = open(WRITE_PATH + "1285647590049125.json")
text = reader.read()
reader.close()
print(getLocation(text), getTweet(text))
print(getLanguage(text))
#writeCoordinates([1,1], "1285127566282033.json", text)
#'''
#nlp = spacy.load('en_core_web_lg')
#sample = open("tweet.txt")
#doc = nlp(sample.read())
#sample.close()
#for ent in doc.ents:
#   if ent.label_ == "LOC" or ent.label_ == "GPE":
#      print(ent.text, ent.label_, str(geocoder.arcgis(ent.text).latlng))
