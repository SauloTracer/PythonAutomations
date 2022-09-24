''' Boiler plate for relative path import'''
# Add's the project root folder to the path so we can import the Auto module normally
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
#########################################################

from Auto import *
import time

WAIT_FOR_GEMS = 10
SAFE_POINT = (5,5)


def spinWheel():
    count = 20
    while True: 
        res = clickImage("./img/wheel.png", (827, 390, 330, 70))
        if res:
            break
        count -= 1
        if count <= 0 or keyboard.is_pressed('q'):
            break
        time.sleep(1)


def main():
    while True:
        spinWheel()
        time.sleep(5)
        CloseAd()
        time.sleep(WAIT_FOR_GEMS)
        if keyboard.is_pressed('q'):
            break


main()