from django.shortcuts import render, HttpResponse
import requests
import json

from requests.api import request
from geopy.geocoders import Nominatim

print("##################################################################################################################################################################################################################")
# Create your views here.


def index(request):
    if request.method == 'POST':
        return render(request, 'results.html')
    else:
        return render(request, 'index.html')


def riskpredictor(request):
    return render(request, 'riskpredictor.html')


def about(request):
    return render(request, 'about.html')


def loading(request):
    return render(request, 'loading.html')


def results(request):
    return render(request, 'results.html')


def contact(request):
    return render(request, 'contact.html')


def vaccine(request):
    if request.method == 'POST':
        pincode = request.POST['pincode']
        date = request.POST['date']
        context=vaccine_tracker(pincode,date)
        return render(request, 'vaccine.html',context)
    else:
        return render(request,'vaccine.html')

def vaccine_tracker(pincode,date):
    try:
        date=str(date)
        temp=list(date.split('-'))
        temp.reverse()
        date="-".join(temp)
        params = {'pincode': pincode, 'date': date}
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
        # URL="https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong"
        # params={'lat':28.72,'long':77.14}
        response = requests.get(url=URL, params=params)  # headers=headers
        data = response.json()
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(pincode)
        # print(location.address)
        display_data=[]
        l=data['sessions'][0].keys()
        data=data['sessions']
        for i in range(len(data)):
            d=dict()
            d['Date']=str(data[i]['date'])
            d['Vaccine']=str(data[i]['vaccine'])
            d['Cost']="INR / Rs."+str(data[i]['fee'])+" "+str(data[i]['fee_type'])
            d['Age']=str(data[i]['min_age_limit'])+"+"
            d['Center Name']=str(data[i]['name'])
            d['Address']=str(data[i]['name'])+" "+str(data[i]['address'])+" "+str(data[i]['block_name'])+" "+str(data[i]['district_name'])+" "+str(data[i]['state_name'])+" "+str(data[i]['pincode'])
            d['Available Dose 1 Quantity']=str(data[i]['available_capacity_dose1'])
            d['Available Dose 2 Quantity']=str(data[i]['available_capacity_dose2'])
            d['Slots']=list(data[i]['slots'])
            display_data.append(d)
        l=list(display_data[0].keys())
        context= {
            'data': display_data,
            'lc': location.address,
            'l':l,
            'slot':'Slots',
        }
    except:
        print("Invalid Operation...!!!")
        context={'error':'Inavlid Operation were Performed...!!!'}
    return context