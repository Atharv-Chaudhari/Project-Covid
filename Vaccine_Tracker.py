import requests
import json

pincode = input("Enter Pincode : ")
date = input("Enter Date : ")

params = {'pincode':pincode,'date':date}

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"

response = requests.get(url=URL, params=params) #headers=headers

data = response.json()
print(json.dumps(data, indent=4))
