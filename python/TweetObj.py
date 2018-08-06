class Tweet(object):
   def __init__(self, json_text, location, file_name):
      self.json_text = str(json_text)
      self.location = location
      self.file_name = file_name
      self.coordinates = ""

   def __str__(self):
      return self.json_text + " " + self.location + " " + self.file_name + " " + self.coordinates

