import geocoder
import redis
import requests

red = redis.Redis(host='localhost', port=6379, password='')
dictionary = {"ALABAMA":"AL",
"ALASKA":"AK",
"ARIZONA":"AZ",
"ARKANSAS":"AR",
"CALIFORNIA":"CA",
"COLORADO":"CO",
"CONNECTICUT":"CT",
"DELAWARE":"DE",
"FLORIDA":"FL",
"GEORGIA":"GA",
"HAWAII":"HI",
"IDAHO":"ID",
"ILLINOIS":"IL",
"INDIANA":"IN",
"IOWA":"IA",
"KANSAS":"KS",
"KENTUCKY":"KY",
"LOUISIANA":"LA",
"MAINE":"ME",
"MARYLAND":"MD",
"MASSACHUSETTS":"MA",
"MICHIGAN":"MI",
"MINNESOTA":"MN",
"MISSISSIPPI":"MS",
"MISSOURI":"MO",
"MONTANA":"MT",
"NEBRASKA":"NE",
"NEVADA":"NV",
"NEW HAMPSHIRE":"NH",
"NEW JERSEY":"NJ",
"NEW MEXICO":" NM",
"NEW YORK":"NY",
"NORTH CAROLINA":"NC",
"NORTH DAKOTA":"ND",
"OHIO":"OH",
"OKLAHOMA":"OK",
"OREGON":"OR",
"PENNSYLVANIA":"PA",
"RHODE ISLAND":"RI",
"SOUTH CAROLINA":"SC",
"SOUTH DAKOTA":"SD",
"TENNESSEE":"TN",
"TEXAS":"TX",
"UTAH":"UT",
"VERMONT":"VT",
"VIRGINIA":"VA",
"WASHINGTON":"WA",
"WEST VIRGINIA":"WV",
"WISCONSIN":"WI",
"WYOMING":"WY"
}
def geocoderCall(location):
   key = str(geocoder.arcgis(location).latlng)
   lat = key[1:key.find(",")]
   lng = key[key.find(",") + 2: len(key) - 1]
   return "[" + lng + ", " +  lat + "]"
'''
key = red.get("wy").decode("utf-8")
lat = key[1:key.find(",")]
lng = key[key.find(",") + 2: len(key) - 1]
print(key)
newval = "[" + lng + ", " +  lat + "]"
print(newval)
print(geocoderCall("virginia"))


keys = red.keys('*')
for key in keys:
   val = red.get(key).decode("utf-8")
   lat = val[1:val.find(",")]
   lng = val[val.find(",") + 2: len(val) - 1]
   newval = "[" + lng + ", " +  lat + "]"
   print(val)
   print(newval)
   red.set(key, newval)

print(red.get("va"))

session = requests.Session()
print(geocoder.arcgis("hells kitchen", session=session).latlng)
print(geocoder.arcgis("vermont", session=session).latlng)
print(geocoder.arcgis("Australia", session=session).latlng)
print(geocoder.arcgis("Norway", session=session).latlng)
print(geocoder.arcgis("Canada", session=session).latlng)
print(geocoder.arcgis("Dublin", session=session).latlng)
print(geocoder.arcgis("fairfax", session=session).latlng)
print(geocoder.arcgis("missouri", session=session).latlng)
print(geocoder.arcgis("mississippi", session=session).latlng)
print(geocoder.arcgis("virginia", session=session).latlng)
session.close()
#print(red.get())
print(geocoder.arcgis("幸村くんの3歩後ろ").latlng) '''
print(red.dbsize())
red.save()
listt = [1,2,3]
out = str(listt).replace("[", "").replace("]", "")
print(out)
temp = {}
temp["virginia"] = ""
for ref_key in temp:
   temp[ref_key] = geocoder.arcgis(ref_key).latlng
   print(ref_key, temp[ref_key])

