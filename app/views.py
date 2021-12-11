from django.shortcuts import render, HttpResponse
import requests
import json
import requests
from bs4 import BeautifulSoup
from requests.api import request
from geopy.geocoders import Nominatim
import time
import joblib
import pandas as pd
print("##################################################################################################################################################################################################################")
# Create your views here.

loaded_model = joblib.load ('model1.sav')

def get_prediction (data,loaded_model = loaded_model):
    data={
        'cough':data['Cough'],
        'fever':data['Fever'],
        'sore_throat':data['Sore_Throat'],
        'shortness_of_breath':data['Shortness_of_Breath'],
        'head_ache':data['Headache'],
        'age_60_and_above':data['age'],
        'abroad':data['Abroad'],
        'contact_with_covid_object':data['contact_Object'],
        'contact_with_covid_patient':data['contact_Patient'],
    }
    df = pd.DataFrame(data,index=[0])
    print(df)
    prediction=loaded_model.predict(df.values)
    pred_prob = loaded_model.predict_proba(df.values)
    print(prediction,pred_prob)
    return pred_prob


wdata=[]
def world_data():
    global wdata
    URL = "https://www.worldometers.info/coronavirus/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup.select(".maincounter-number span"))
    nums = soup.find_all('div', attrs={'class': 'maincounter-number'})
    wdata=[]
    for tag in nums:
        wdata.append(tag.text.strip())

# while True:
#     world_data()
#     time.sleep(2)

def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    global wdata
    if request.method == 'POST':
        model_data=request.POST
        context={
            'model_pred':get_prediction(model_data)
        }
        return render(request, 'results.html',context)
    else:
        world_data()
        d={
            'cases':wdata[0],
            'deaths':wdata[1],
            'recovered':wdata[2]
        }
        return render(request, 'index.html',d)
        # return render(request, 'index.html')


def riskpredictor(request):
    if request.method == 'POST':
        # print(request.POST)
        # get_prediction()
        return render(request, 'results.html')
    else:
        return render(request, 'riskpredictor.html')


def about(request):
    return render(request, 'about.html')


def dashboard(request):
    return render(request, 'dashboard.html')


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
        context={'error':'Invalid Operations were Performed...!!!'}
    return context