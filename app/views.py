from django.shortcuts import redirect, render, HttpResponse
import requests
import json
import requests
from bs4 import BeautifulSoup
from requests.api import request
from django.http import HttpResponseRedirect
# from .forms import UploadFileForm
from geopy.geocoders import Nominatim
from time import sleep
import joblib
import pandas as pd
from .task import *
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from keras.models import load_model
import cv2
# import tensorflow as tf
# from keras.preprocessing import image
# from datetime import date
# today = date.today()
# update_date=today.strftime("%d %b %Y").split()
# print(update_date)
from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf 
 
# from apscheduler.schedulers.background import BackgroundScheduler

print("################################################## Lets Start Project #############################################################")
# Create your views here.

loaded_model = joblib.load('models/model1.sav')

#Creating our view, it is a class based view
class GeneratePdf(View):
     def get(self, request):
        with open("tmp/pdf/report_one.txt",'rb') as f:
            result = f.read()
        return HttpResponse(result, content_type='application/pdf')

def get_prediction(data, loaded_model=loaded_model):
    data_model = {
        'cough': data['Cough'],
        'fever': data['Fever'],
        'sore_throat': data['Sore_Throat'],
        'shortness_of_breath': data['Shortness_of_Breath'],
        'head_ache': data['Headache'],
        'age_60_and_above': data['age'],
        'gender': data['Gender'],
        'abroad': data['Abroad'],
        'contact_with_covid_patient': data['contact_Patient']
    }
    df = pd.DataFrame(data_model, index=[0])
    print(df)
    prediction = loaded_model.predict(df.values)
    pred_prob = loaded_model.predict_proba(df.values)
    print(prediction, pred_prob)
    for x in data_model.keys():
        if(x == 'gender'):
            if(data_model['gender'] == '1'):
                data_model[x] = "Male"
            else:
                data_model[x] = "Female"
        else:
            if(data_model[x] == '1'):
                data_model[x] = "Yes"
            else:
                data_model[x] = "No"
    data_model['prob'] = str(int(pred_prob[0][1]*100))+" %"
    data_model['prediction'] = str(prediction[0])
    data_model['email'] = data['email']
    data_model['country'] = data['country']
    if(data_model['country'] == ''):
        data_model['country'] = "Not Given"
    data_model['one'] = ['Yes', '1']
    send_mail_task.delay(data_model)
    report_one.delay(data_model)
    # ctx = {
    #     'data': data,
    # }
    # messageContent = get_template('email.html').render(ctx)
    # file = open("templates/report_one.html","w")
    # file.write(str(messageContent))
    # file.close()
    # print(str(messageContent))
    return data_model

# data refresher for replit
# def refresher():
#     world_data.delay(0)
#     return

# scheduler = BackgroundScheduler()
# job = scheduler.add_job(refresher, 'interval', minutes=60)
# scheduler.start()


# wdata=[]
# def world_data():
#     global wdata
#     URL = "https://www.worldometers.info/coronavirus/"
#     r = requests.get(URL)

#     soup = BeautifulSoup(r.content, 'html5lib')
#     # print(soup.select(".maincounter-number span"))
#     nums = soup.find_all('div', attrs={'class': 'maincounter-number'})
#     wdata=[]
#     for tag in nums:
#         wdata.append(tag.text.strip())

# while True:
#     world_data()
#     time.sleep(2)

def email(request):
    context={
        'data': get_prediction({'csrfmiddlewaretoken': ['UI5kSD5v9KtSLSw9hU9b2zYhw9433kkmj9XL4FBoStD1HOsdRjIcF0gam8xErb34'], 'form_type': ['formFour'], 'email': ['atharv3820@gmail.com'], 'country': [''], 'Gender': ['1'], 'age': ['0'], 'Cough': ['0'], 'Fever': ['0'], 
'Sore_Throat': ['0'], 'Shortness_of_Breath': ['0'], 'Headache': ['0'], 'Abroad': ['0'], 'contact_Patient': ['0']})
    }
    return render(request, 'email.html',context)


def welcome(request):
    return render(request, 'welcome.html')


def update(request):
    world_data.delay(0)
    sleep(5)
    return redirect('home')


def home(request):
    # global wdata
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    else:
        # global update_date
        world_data.delay(0)
        f = open("tmp/data.json", "r")
        d = json.load(f)
        # d["update_dt"]=update_date[0]
        # d["update_mn"]=update_date[1]
        # d["update_yr"]=update_date[2]
        return render(request, 'index.html', d)
        # return render(request, 'index.html')


def riskpredictor(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
        elif request.POST.get("form_type") == 'formSix':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    else:
        return render(request, 'riskpredictor.html')


def about(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    return render(request, 'about.html')


def dashboard(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    return render(request, 'dashboard.html')


def loading(request):
    return render(request, 'spinner.html')


def results(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    return render(request, 'results.html')


def contact(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
    return render(request, 'contact.html')


def vaccine(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
        elif request.POST.get("form_type") == 'formFive':
            pincode = request.POST['pincode']
            date = request.POST['date']
            context = vaccine_tracker(pincode, date)
            return render(request, 'vaccine.html', context)
    else:
        return render(request, 'vaccine.html')


def vaccine_tracker(pincode, date):
    try:
        date = str(date)
        temp = list(date.split('-'))
        temp.reverse()
        date = "-".join(temp)
        params = {'pincode': pincode, 'date': date}
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
        # URL="https://cdn-api.co-vin.in/api/v2/appointment/centers/public/findByLatLong"
        # params={'lat':28.72,'long':77.14}
        response = requests.get(url=URL, params=params,headers=headers)  # headers=headers
        data = response.json()
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(pincode)
        # print(location.address)
        display_data = []
        l = data['sessions'][0].keys()
        data = data['sessions']
        for i in range(len(data)):
            d = dict()
            d['Date'] = str(data[i]['date'])
            d['Vaccine'] = str(data[i]['vaccine'])
            d['Cost'] = "INR / Rs." + \
                str(data[i]['fee'])+" "+str(data[i]['fee_type'])
            d['Age'] = str(data[i]['min_age_limit'])+"+"
            d['Center Name'] = str(data[i]['name'])
            d['Address'] = str(data[i]['name'])+" "+str(data[i]['address'])+" "+str(data[i]['block_name']) + \
                " "+str(data[i]['district_name'])+" "+str(data[i]
                                                          ['state_name'])+" "+str(data[i]['pincode'])
            d['Available Dose 1 Quantity'] = str(
                data[i]['available_capacity_dose1'])
            d['Available Dose 2 Quantity'] = str(
                data[i]['available_capacity_dose2'])
            d['Slots'] = list(data[i]['slots'])
            display_data.append(d)
        l = list(display_data[0].keys())
        context = {
            'data': display_data,
            'lc': location.address,
            'l': l,
            'slot': 'Slots',
        }
    except:
        print("Invalid Operation...!!!")
        context = {'error': 'No Data Available'}
    return context


def welcome_dashboard(request):
    return render(request, 'welcome_dashboard.html')

def img_process(img):
    model_1 = load_model('models/cnn_model.h5')

    z_img = cv2.imread(img)
    z_img = cv2.resize(z_img, (70, 70)) / 255.0
    z_img = z_img.reshape(1, z_img.shape[0], z_img.shape[1], z_img.shape[2])
        
    z = model_1.predict(z_img)
    z = np.argmax(z, axis = 1)
    return z

def img_pred(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'model_pred': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
        if request.POST.get("form_type") == 'formSeven' and request.FILES['image']:
            filename = request.FILES['image']
            filename=str(filename)
            file_data=request.FILES['image'].read()
            temp=filename.index(".")
            img="tmp/image"+str(filename[temp:])
            with open("tmp/image"+str(filename[temp:]), "wb") as outfile:
                outfile.write(file_data)
            imgpred=img_process(img)
            return render(request, 'img_result.html',{'imgpred':imgpred})
    return render(request, 'img_pred.html')
    
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
def predictors(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formFour':
            model_data = request.POST
            context = {
                'data': get_prediction(model_data)
            }
            return render(request, 'results.html', context)
        if request.POST.get("form_type") == 'formSeven' and request.FILES['image']:
            filename = request.FILES['image']
            filename=str(filename)
            file_data=request.FILES['image'].read()
            temp=filename.index(".")
            img="static/tmp/image"+str(filename[temp:])
            print(img)
            with open("static/tmp/image"+str(filename[temp:]), "wb") as outfile:
                outfile.write(file_data)
            imgpred=img_process(img)
            file_n="static/tmp/image"+str(filename[temp:])
            tk=[1]
            return render(request, 'img_result.html',{'imgpred':imgpred[0],'img_result':file_n,'tk':tk})
    return render(request, 'predictors.html')

def nlp(request):
    return render(request, 'nlp.html')