from flask import Flask
from bs4 import BeautifulSoup
from selenium import webdriver

import os
import time
import pyautogui
import random
import requests

app = Flask(__name__)

@app.route("/party")
def essential():
    os.system('displayswitch /clone')
    time.sleep(3)

    url = 'https://www.youtube.com/playlist?list=PLKRZTF1Q1uwbkyqPDcZDF4y-_TLUYy7r8'
    tag_class = 'ytd-playlist-video-renderer'
    max_range = 10
    bgm = selesoup(url, tag_class, max_range)
    play(bgm)
    return 'clear'
       
@app.route("/partyover")
def partyover():
    pyautogui.press('space')
    os.system('displayswitch /extend')
    return 'clear'

@app.route("/cafe")
def cafe():
    url = 'https://www.youtube.com/results?search_query=cafe+jazz'
    tag_class = 'ytd-video-renderer'
    max_range = 30
    bgm = selesoup(url, tag_class, max_range)
    play(bgm)
    return 'clear'

@app.route("/dashboard")
def dashboard():
    os.system('start chrome --new-window --start-maximized \
        http://localhost:5601/app/kibana#/dashboard/bf77d170-4e46-11eb-97ef-b13db7bc9238')
    return 'clear'

def selesoup(url, tag_class, max_range):
    driver = webdriver.Chrome('/Users/under/tools/chromedriver')
    driver.implicitly_wait(3)
    driver.get(url)
    complete_html = driver.page_source

    soup = BeautifulSoup(complete_html, 'html.parser')
    renderers = soup.find_all('a', {'class': tag_class})
    path = renderers[random.randint(1, max_range)]['href']
    bgm = 'youtube.com' + path
    return bgm

def play(bgm):
    os.system('start chrome --new-window --start-maximized ' + bgm)
    time.sleep(5)
    pyautogui.press('f')

if __name__ == '__main__':
    app.run(host='0.0.0.0')