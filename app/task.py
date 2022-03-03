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
    repo = g.get_user().get_repo('Project-Covid-Helper')
    file_list = [
        data['img'],
        data['img'].replace("image","cam_pred"),
    ]
    file_names = [
        data['img'],
        data['img'].replace("image","cam_pred"),
    ]
    commit_message = 'Commit Images'
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        if entry.endswith('.png'): 
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
    ctx = {
        'tk':[1],
        'output': int(data['output']),
        'email':data['email'],
        'img':'',
        'cam_img':'',
    }
    heading = "Test Report By Team InfySOARS"
    messageContent = get_template('img_email.html').render(ctx)
    msg = EmailMessage(heading, messageContent, '<infysoars0@gmail.com>',
                       [data['email']])
    msg.content_subtype = 'html'
    msg.send()
    return None