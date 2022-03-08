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
from github import Github
from github import InputGitTreeElement
import os


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
    return None


@shared_task
def world_data(d):
    URL = "https://www.worldometers.info/coronavirus/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
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
    return None


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
    password = os.environ.get("email_pass")

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
    return None
