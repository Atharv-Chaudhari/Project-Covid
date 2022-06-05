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
from .gradcam import *
# importing get_template from loader
from django.template.loader import get_template
from PIL import Image
import base64
import io
import base64
# from github import Github
# from github import InputGitTreeElement
import os
from django.conf import settings
import mysql.connector
mydb = mysql.connector.connect(
            database=getattr(settings, "DB_USER", None),
            host="remotemysql.com",
            user=getattr(settings, "DB_USER", None),
            password=getattr(settings, "DB_PASS", None),
            port=3306
        )
cursor = mydb.cursor()

@shared_task
def saveme(cough,fever,sore_throat,shortness_of_breath,head_ache,age_60_and_above,gender,abroad,contact_with_covid_patient,prob,pred,email, country):
    mydb = mysql.connector.connect(
            database=getattr(settings, "DB_USER", None),
            host="remotemysql.com",
            user=getattr(settings, "DB_USER", None),
            password=getattr(settings, "DB_PASS", None),
            port=3306
        )
    cursor = mydb.cursor()
    if(pred==0):
        prediction="Negative"
    else:
        prediction="Positive"
    try:
        tempo=(cough,fever,sore_throat,shortness_of_breath,head_ache,age_60_and_above,gender,abroad,contact_with_covid_patient,prob,prediction,email, country)
        query1='''Insert into phase1(cough,fever,sore_throat,shortness_of_breath,head_ache,age_60_and_above,gender,abroad,contact_with_covid_patient,prob,prediction,email, country) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        cursor.execute(query1,tempo)
        print("Data has been Saved Successfully...!!")
    except mysql.connector.Error as e:
        print(e)
    mydb.commit()

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
    msg = EmailMessage(heading, messageContent, '<infysoars0@gmail.com>',
                       [data['email']])
    msg.content_subtype = 'html'
    msg.send()
    print("Phase 1 Email sent successfully...!!!")
    return None


@shared_task
def world_data(d):
    URL = "https://www.worldometers.info/coronavirus/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')
    nums = soup.find_all('div', attrs={'class': 'maincounter-number'})
    wdata = []
    for tag in nums:
        wdata.append(tag.text.strip())
    d = {
        'cases': wdata[0],
        'deaths': wdata[1],
        'recovered': wdata[2]
    }
    f = open("static/tmp/data.json", "w")
    f = json.dump(d, f)
    print("Data Scrapped Successfully...!!!")
    return None

@shared_task
def savemyimg(email,original_img,gradcam_img):
    mydb = mysql.connector.connect(
            database=getattr(settings, "DB_USER", None),
            host="remotemysql.com",
            user=getattr(settings, "DB_USER", None),
            password=getattr(settings, "DB_PASS", None),
            port=3306
        )
    cursor = mydb.cursor()
    original_img = base64.b64encode(open(original_img,'rb').read())
    gradcam_img = base64.b64encode(open(gradcam_img,'rb').read())
    try:
        tempo=(email,original_img,gradcam_img)
        query1='''Insert into phase2a values (%s,%s,%s);'''
        cursor.execute(query1,tempo)
    except mysql.connector.Error as e:
        print(e)
    
    mydb.commit()
    print("Saving Phase 2 X-Ray Successfull...!!!")

@shared_task
def savemyimg2(email,original_img,gradcam_img):
    mydb = mysql.connector.connect(
            database=getattr(settings, "DB_USER", None),
            host="remotemysql.com",
            user=getattr(settings, "DB_USER", None),
            password=getattr(settings, "DB_PASS", None),
            port=3306
        )
    cursor = mydb.cursor()
    original_img = base64.b64encode(open(original_img,'rb').read())
    gradcam_img = base64.b64encode(open(gradcam_img,'rb').read())
    try:
        tempo=(email,original_img,gradcam_img)
        query1='''Insert into phase2b values (%s,%s,%s);'''
        cursor.execute(query1,tempo)
    except mysql.connector.Error as e:
        print(e)
    
    mydb.commit()
    print("Saving Phase 2 CT Scan Successfull...!!!")

@shared_task
def send_img_mail_task(data):
    cam_pred(data['img'], data['img'].replace("image", "cam_pred"))
    ctx = {
        'tk': [1],
        'output': int(data['output']),
        'email': data['email'],
        'img':str(data['img'].split("/")[-1]),
        'cam_img':str(data['img'].replace("image", "cam_pred").split("/")[-1]),
    }
    # heading = "Test Report By Team InfySOARS"
    savemyimg.delay(ctx['email'],data['img'],data['img'].replace("image", "cam_pred"))
    messageContent = get_template('img_email.html').render(ctx)
    # msg = EmailMessage(heading, messageContent, '<infysoars0@gmail.com>',
    #                    [data['email']])
    # msg.content_subtype = 'html'
    # msg.send()

    import smtplib
    import ssl
    import email
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "infysoars0@gmail.com"
    receiver_email = data['email']
    password = getattr(settings, "EMAIL_PASS", None)

    # Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Test Report By Team InfySOARS"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    filename = [data['img'],
                data['img'].replace("image", "cam_pred")]

    part = MIMEText(messageContent, "html")
    msg.attach(part)

    # Add Attachment
    for i in range(len(filename)):
        with open(filename[i], "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            encoders.encode_base64(part)

            # Set mail headers
            part.add_header(
                "Content-Disposition",
                "attachment", filename=filename[i].split("/")[-1]
            )
            part.add_header('Content-ID', '<'+filename[i].split("/")[-1]+'>')
            msg.attach(part)

    # Create secure SMTP connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
    print("Phase 2 Email sent successfully...!!!")
    return None

@shared_task
def send_img_mail_task2(data):
    cam_pred(data['img'], data['img'].replace("image", "cam_pred"))
    ctx = {
        'tk': [1],
        'output': int(data['output']),
        'email': data['email'],
        'img':str(data['img'].split("/")[-1]),
        'cam_img':str(data['img'].replace("image", "cam_pred").split("/")[-1]),
    }
    # heading = "Test Report By Team InfySOARS"
    savemyimg2.delay(ctx['email'],data['img'],data['img'].replace("image", "cam_pred"))
    messageContent = get_template('img_email 2.html').render(ctx)
    # msg = EmailMessage(heading, messageContent, '<infysoars0@gmail.com>',
    #                    [data['email']])
    # msg.content_subtype = 'html'
    # msg.send()

    import smtplib
    import ssl
    import email
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "infysoars0@gmail.com"
    receiver_email = data['email']
    password = getattr(settings, "EMAIL_PASS", None)

    # Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Test Report By Team InfySOARS"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    filename = [data['img'],
                data['img'].replace("image", "cam_pred")]

    part = MIMEText(messageContent, "html")
    msg.attach(part)

    # Add Attachment
    for i in range(len(filename)):
        with open(filename[i], "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            encoders.encode_base64(part)

            # Set mail headers
            part.add_header(
                "Content-Disposition",
                "attachment", filename=filename[i].split("/")[-1]
            )
            part.add_header('Content-ID', '<'+filename[i].split("/")[-1]+'>')
            msg.attach(part)

    # Create secure SMTP connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
    print("Phase 2 Email sent successfully...!!!")
    return None
