import pyautogui as pg
import time
import keyboard
import random
import win32api, win32con

#    Extract text from screen area
#    Select and position a specific team
#    Identify how much is needed to buy a specific upgrade
updateTime = 0.5
# runType = "kn5"
runType = "gold"

areas = {
    "tr": (1090, 30, 106, 80),
    "center": (700, 500, 500, 150),
    "dc": (800, 720, 300, 100)
}

buttons = {
    "kn": (812, 363),       # king normal
    "jrh": (962, 724),      # joint revenge hard
    "go": (959, 978),       # Confirm formation
    "wave": (1142, 68)      # Wave
}

images = {
    "coin": "img/coin.png",
    "ad": "img/ad.png",
    "continue": "img/continue.png",
    "exit": "img/exit.png",
    "ok": "img/ok.png",
    "classic": "img/classic.png",
}


def esc():
    print("esc")
    click((5, 100))
    keyboard.press_and_release('esc')
    if(findImage(images["exit"], areas["center"])):
        keyboard.press_and_release('esc')


def buy(point):
    print("buy")
    click(point)
    time.sleep(2)
    esc()    
        

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


def restart():
    print("restart")

    click(buttons["wave"])
    time.sleep(1)
    start()


def start():
    print("start")

    global runType
    level = None

    if(runType == "gold"):
        level = buttons["jrh"]
    elif(runType == "kn5"):
        level = buttons["kn"]

    click(level)
    time.sleep(2.5)
    click(buttons["go"])


def loop():
    print("loop")

    global runType
    global updateTime

    while True:
        if keyboard.is_pressed("q"):
            break

        if(findImage(images["ad"], areas["center"])):
            time.sleep(1)
            esc()

        if(point := findImage(images["coin"], areas["center"])):
            time.sleep(1)
            buy(point)
            if(runType == "kn5"):
                restart()
        
        if(point := findImage(images["continue"], areas["dc"])):
            time.sleep(1)
            click(point)
            time.sleep(2)
            start()
        
        time.sleep(updateTime)


def main():
    print("main")
    start()
    loop()


main()