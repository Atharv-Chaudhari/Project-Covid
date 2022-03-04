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
#importing get_template from loader
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
    cam_pred(data['img'],data['img'].replace("image","cam_pred"))
    
    token = os.environ['token']
    g = Github(token)
    repo = g.get_user().get_repo('Project-Covid-Helper') # repo name
    print(repo)
    file_list = [
        data['img'],
        data['img'].replace("image","cam_pred")
    ]
    file_names = [
        str(list(data['img'].split('/'))[-1]),
        str(list(data['img'].replace("image","cam_pred").split('/'))[-1])
    ]
    commit_message = 'python commit'
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry,'rb') as input_file:
            data1 = input_file.read()
        if entry.endswith('.png'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.jpeg'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.jfif'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.pjpeg'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.bmp'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.webp'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.pjp'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.tif'): 
            data1 = base64.b64encode(data1)
        if entry.endswith('.jpg'): 
            data1 = base64.b64encode(data1)
        blob = repo.create_git_blob(data1.decode("utf-8"), "base64")
        element = InputGitTreeElement(file_names[i], mode='100644', type='blob',sha=blob.sha)
        element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
    import time
    time.sleep(10)
    ctx = {
        'tk':[1],
        'output': int(data['output']),
        'email':data['email'],
        'img':str("https://raw.githubusercontent.com/INFYSOARS/Project-Covid-Helper/main/")+file_names[0],
        'cam_img':str("https://raw.githubusercontent.com/INFYSOARS/Project-Covid-Helper/main/")+file_names[1],
    }
    heading = "Test Report By Team InfySOARS"
    messageContent = get_template('img_email.html').render(ctx)
    msg = EmailMessage(heading, messageContent, '<infysoars0@gmail.com>',
                       [data['email']])
    msg.content_subtype = 'html'
    msg.send()
    return None