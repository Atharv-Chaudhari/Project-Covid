import requests
import json

from requests.api import request
from geopy.geocoders import Nominatim

pincode = input("Enter Pincode : ")
date = input("Enter Date : ")

params = {'pincode':pincode,'date':date}

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
# URL="https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong"
# params={'lat':28.72,'long':77.14}
response = requests.get(url=URL, params=params) #headers=headers

data = response.json()
print(json.dumps(data, indent=4))

geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.geocode(pincode)
print(location.address) 
