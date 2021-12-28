from celery import shared_task
from time import sleep
from django.template.loader import get_template
from django.core.mail import EmailMessage
import requests
from bs4 import BeautifulSoup
import json
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf 
 
# from fpdf import FPDF, HTMLMixin


# class PDF(FPDF, HTMLMixin):
#     pass


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_mail_task(data):
    ctx = {
        'data': data,
    }
    heading = "Test Report By Team InfySOARS"
    messageContent = get_template('email.html').render(ctx)
    msg = EmailMessage(heading, messageContent, 'infysoars0@gmail.com',
                       [data['email']])
    msg.content_subtype = 'html'
    msg.send()
    return None


@shared_task
def report_one(data):
    # ctx = {
    #     'data': data,
    # }
    # messageContent = get_template('report_one.html').render(ctx)
    # pdf = PDF()
    # pdf.add_page()
    # pdf.write_html(messageContent)
    # pdf.output('pdf/report_one.pdf')
    ctx = {
        'data': data,
    }
        #getting the template
    pdf = render_to_pdf('report_one.html',ctx)
    with open("pdf/report_one.txt", "wb") as outfile:
        outfile.write(pdf.getvalue())
    return None


@shared_task
def world_data(d):
    URL = "https://www.worldometers.info/coronavirus/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup.select(".maincounter-number span"))
    nums = soup.find_all('div', attrs={'class': 'maincounter-number'})
    wdata = []
    for tag in nums:
        wdata.append(tag.text.strip())
    d = {
        'cases': wdata[0],
        'deaths': wdata[1],
        'recovered': wdata[2]
    }
    f = open("data.json", "w")
    f = json.dump(d, f)
    return None
