from flask import Flask
import os
import time
import pyautogui
import random

app = Flask(__name__)

@app.route("/party")
def essential():
    os.system('displayswitch /clone')
    time.sleep(3)

    # os.system('taskkill /F /IM chrome.exe')
    # time.sleep(1)

    os.system('start chrome --new-window --start-maximized \
        https://www.youtube.com/playlist?list=PLKRZTF1Q1uwbkyqPDcZDF4y-_TLUYy7r8')
    time.sleep(5)

    x, y = randomset()
    pyautogui.click(x, y)
    time.sleep(2)

    pyautogui.press('f')
    return 'clear'
       
@app.route("/partyover")
def partyover():
    pyautogui.press('space')
    os.system('displayswitch /extend')
    return 'clear'

def randomset():
    x = 750
    y = list(range(220, 1021, 100))
    y_select = random.choice(y)
    return x, y_select

if __name__ == '__main__':
    app.run(host='0.0.0.0')