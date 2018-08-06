class Tweet(object):
    def __init__(self, json_text, location, file_name):
        self.json_text = json_text
        self.location = location
        self.file_name = file_name
        self.coordinates = ""
