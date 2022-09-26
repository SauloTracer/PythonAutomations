import pyautogui as pg
from math import floor
import time
import keyboard
import win32api, win32con
import json
from .Point import *
from .Area import *


def click(point : Point, resetMousePos : Point=None, wait:float=0.03):
    # print("click", point)
    win32api.SetCursorPos(point)
    time.sleep(wait) #This pauses the script for wait seconds to avoid missing the click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(wait) #This pauses the script for wait seconds to avoid missing the click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    if resetMousePos != None:
        win32api.SetCursorPos(resetMousePos)


def findImage(image : str, area : Area, confidence:float=0.9, tries:int=1, wait:float=0.1):
    # print('Searching for image: ' + image)
    try:
        for i in range(tries):
            point = pg.locateCenterOnScreen(image, region=area, confidence=confidence)
            if point:
                return point
            time.sleep(wait)
        return point
    except:
        return False


def waitForImage(image : str, area : Area, limit:int=60, confidence:float=0.9, wait:float=1):
    while not (point := findImage(image, area, confidence)) or limit <= 0:
        time.sleep(wait)
        limit -= 1
    else:
        return point


def clickImage(image : str, area : Area, confidence:float=0.9):
    # print('clickImage', image)
    point = findImage(image, area, confidence)
    if point:
        click(point)
        return True
    else:
        return False


def drag(startPoint : Point, endPoint : Point, wait:float=0.1):
    win32api.SetCursorPos(startPoint)
    x, y = endPoint
    pg.dragTo(x, y, 1, button='left')
    time.sleep(wait) # wait for drag to finish
    # print("scrollDown finished")


def esc(targetWindowPoint : Point=None):
    if targetWindowPoint:
        click(targetWindowPoint)
    keyboard.press_and_release('esc')


def loadAds():
    ads = {}
    with open("../Auto/ads.json", "r") as f:
        ads = json.load(f)
    return ads


def findAndClickCloseButton(ad):
    res = findImage(ad["img"], ad["area"], 0.8)
    if res:
        if ad["point"] is None:
            clickImage(ad["imgClose"], ad["area"])
        else:
            click(ad["point"])
    return res


def closeAd(outImage : str=None, area : Area=None, confidence:float=0.9):
    all = loadAds()
    ads = filter(lambda ad: not ad["continue"], all)
    continuousAds = filter(lambda ad: ad["continue"], all)
    iteration = 0
    while True:
        iteration += 1
        print("Iteration: ", iteration)
        foundClose = False
        foundContinue = False

        for ad in ads:
            if keyboard.is_pressed('q'):
                break # break out of for loop and continues while loop flow
            foundClose = findAndClickCloseButton(ad)
            if foundClose:
                break # break out of for loop and continues while loop flow

        time.sleep(6)

        for cad in continuousAds:
            if keyboard.is_pressed('q'):
                break # break out of for loop and continues while loop flow
            foundContinue = findAndClickCloseButton(cad)
            if foundContinue:
                break # break out of for loop and continues while loop flow
        
        if foundClose and not foundContinue:
            return
        
        if findImage(outImage, area, confidence):
            return

        if keyboard.is_pressed('q'):
            break



def areaFromPoint(point : Point, width : int=None, height : int=None):
    if width is None:
        width = 1
    if height is None:
        height = width
    x, y = point
    x -= floor(width / 2)
    y -= floor(height / 2)
    return (x, y, width, height)