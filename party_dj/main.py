import time
from fastapi import FastAPI

import random
import pyautogui
import requests
import re
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello DJ"}

@app.get("/party")
def essential():
    YOUTUBE = 'https://www.youtube.com/'
    url = 'https://www.youtube.com/playlist?list=PLKRZTF1Q1uwbkyqPDcZDF4y-_TLUYy7r8'

    res = requests.get(url)
    text = res.text
    watch_index_list = [m.start() for m in re.finditer('watch\?', text)]

    target_list = []
    for i, index in enumerate(watch_index_list):
        candidate = text[index:index+80]
        options = candidate.split('"')
        target_list.append(options[0])
        if i > 50:
            break

    random.shuffle(target_list)
    selected_bgm = YOUTUBE + target_list[0]
    _play(selected_bgm)
    return 'clear'

def _play(bgm):
    os.system('open -a "Google Chrome" ' + bgm)
    time.sleep(5)
    pyautogui.press('f')

@app.get("/partyover")
def partyover():
    pyautogui.press('space')
    time.sleep(5)
    pyautogui.press('f')
    return 'clear'