from math import floor
import pyautogui as pg
import time
import keyboard
import win32api, win32con

WAIT_FOR_GEMS = 10

# imageToFind, point to click, area to search
ads = [
    ("./img/granted.png", (1171,62), (1010, 44, 185, 50)),
    ("./img/leftgranted.png", (745,62), (765, 46, 185, 50)),
    ("./img/granted2.png", (1171,62), (1010, 44, 185, 50)),
    ("./img/close2.png", (1171,62), (1150, 42, 42, 50)),
    ("./img/close3.png", (1172,61), (1150, 42, 42, 50)),
    ("./img/close4.png", (1154,83),  (1125, 53, 55, 57)),
    ("./img/close5.png", (1172,61), (1150, 42, 42, 50)),
    ("./img/close6.png", (1172,65), (1152, 45, 40, 40)),
    ("./img/close7.png", (1172,65), (1154, 42, 40, 42)),
    ("./img/close8.png", (1172,65), (1150, 40, 45, 45)),
    ("./img/close9.png", (748,71), (728, 51, 40, 40)),
    ("./img/close10.png", (1172,65), (1154, 42, 40, 42)),
    ("./img/close11.png", (1172,65), (1149, 42, 53, 42)),
    ("./img/close12.png", (1162,110), (1140, 89, 44, 42)),
    ("./img/close13.png", (1154,73), (1134, 54, 45, 50)),
    ("./img/gplay.png", None, (730, 107, 458, 330), "./img/closeGplay.png"),
    ("./img/wheel.png", (986,422),  (827, 390, 330, 70))
]

def click(point): # point = (x, y)
    print("click", point)
    win32api.SetCursorPos(point)
    time.sleep(0.03) #This pauses the script for 0.02 seconds to avoid missing the click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.03) #This pauses the script for 0.02 seconds to avoid missing the click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    win32api.SetCursorPos((5,5))


def findImage(image, area, confidence=0.9, tries=1):
    print('Searching for image: ' + image)
    try:
        for i in range(tries):
            point = pg.locateCenterOnScreen(image, region=area, confidence=confidence)
            if point:
                return point
            time.sleep(0.1)
        return point
    except:
        return False


def clickImage(image, area, confidence=0.9):
    print('clickImage', image)
    point = findImage(image, area, confidence)
    if point:
        click(point)
        return True
    else:
        return False


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


def resolveAd():
    while True:
        for ad in ads:
            res = findImage(ad[0], ad[2])
            if res:
                if ad[1] is None:
                    clickImage(ad[3], ad[2])
                else:
                    click(ad[1])
                return
            if keyboard.is_pressed('q'):
                break
            time.sleep(0.5)

def main():
    while True:
        spinWheel()
        time.sleep(5)
        resolveAd()
        time.sleep(WAIT_FOR_GEMS)
        if keyboard.is_pressed('q'):
            break


main()