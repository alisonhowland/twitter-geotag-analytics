# A small Object used to store the data necessary for TweetThread to work
class Tweet(object):
   def __init__(self, json_text, location, file_name, ref_locations):
      self.json_text = str(json_text)
      self.location = location
      self.file_name = file_name
      self.coordinates = ""
      self.ref_locations = ref_locations

   def __str__(self):
      return self.json_text + " " + self.location + " " + self.file_name + " " + self.coordinates

