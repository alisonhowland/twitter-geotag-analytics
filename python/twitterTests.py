import unittest
import location

with open("/var/local/code/sampleJSON/sampleIn.json", "r") as json:
   json_text = json.read()

class TestTwitter(unittest.TestCase):

   def testHasTweet(self):
      self.assertTrue(location.hasTweet(json_text))

   def testGetTweet(self):
      self.assertEqual(location.getTweet(json_text), "@nikki_nola_ @KPeynado22 Idk why people have a hard time understanding its savory and nothing else. They can get cl… https://t.co/Fa1gpDu27S")

   def testGetLanguage(self):
      self.assertEqual(location.getLanguage(json_text), "en")

   def testGetLocation(self):
      self.assertEqual(location.getLocation(json_text), "Philly ➡️ D[M]V")


   def testSetLocation(self):
      loc = "anywhere"
      new_text = location.setLocation(loc, json_text)
      self.assertEqual(loc, location.getLocation(new_text))

   def testHasLocation(self):
      self.assertTrue(location.hasLocation(json_text))

   def testSwapCoordinates(self):
      self.assertEqual(location.swapCoordinates("[1.1, 2.2]"), "[2.2, 1.1]")
      self.assertEqual(location.swapCoordinates(None), None)
      self.assertEqual(location.swapCoordinates("None"), None)
