from math import floor
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
    "dc": (800, 720, 300, 100),
    "formation": (796,325, 327, 386),
    "monsterSelection": (732,208, 82, 751),
    "exitArea": (917, 298, 81, 39)
}

points = {
    "kn": (812, 363),       # king normal
    "jrh": (962, 724),      # joint revenge hard
    "go": (959, 978),       # Confirm formation
    "wave": (1142, 68),     # Wave
    "pos1": (846, 260),     # Position 1
    "pos2": (965, 263),     # Position 2
    "pos3": (1079, 262),    # Position 3
    "pos4": (846, 435),     # Position 4
    "pos5": (965, 435),     # Position 5
    "pos6": (1077, 435),    # Position 6
    "pos7": (849, 610),     # Position 7
    "pos8": (965, 610),     # Position 8
    "pos9": (1077, 610),    # Position 9
}

images = {
    "coin": "img/coin.png",
    "ad": "img/ad.png",
    "continue": "img/continue.png",
    "exit": "img/exit.png",
    "ok": "img/ok.png",
    "classic": "img/classic.png",
    "remove": "img/remove.png",
}

mosnters = {
    "speedy": "img/speedy.png",
    "kevin": "img/kevin.png",
    "neko": "img/neko.png",
    "volt": "img/volt.png",
    "deathByte": "img/deathByte.png",
    "kingSlime": "img/kingSlime.png",
    "kingsLover": "img/kingsLover.png",
    "crispy": "img/crispy.png",
    "felina": "img/felina.png",
    "hellHound": "img/hellHound.png",
    "ra": "img/ra.png",
    "icy": "img/icy.png",
    "iceDragon": "img/iceDragon.png",
    "iceAngel": "img/iceAngel.png",
}

formations = {
    "main": [
        "neko", "kevin", "speedy", 
        "volt", "deathByte", "kingSlime", 
        "crispy", "felina", "hellHound"
    ]
}


def setMonster(monster, position):
    click(position)
    time.sleep(5)
    while not (point := findImage(mosnters[monster], areas["monsterSelection"])):
        scrollDown()
    if point:
        click(point)


def setFormation(formation):
    clearFormation()
    for i in range(len(formation)):
        setMonster(formation[i], points["pos"+str(i + 1)])
        time.sleep(5)


def clearFormation():
    while point := findImage(images["remove"], areas["formation"]):
        click(point)
        time.sleep(1)


def scrollDown():
    win32api.SetCursorPos((1180,930))
    pg.dragTo(1180, 500, 1, button='left')
    time.sleep(7) # wait for scroll to finish
    print("scrollDown finished")

    # """Click and drag x0 y0 to x1 y1"""
    # x = 1180
    # y0, y1 = (930, 630)
    # steps = 20
    # speed = 0.1
    # step = floor((y0 - y1) / steps)
    # win32api.SetCursorPos((x,y0))
    # time.sleep(0.03) #This pauses the script for 0.03 seconds to avoid missing the click
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y0,0,0)
    # for s in range(steps):
    #     win32api.SetCursorPos((x, y0 - step * s))
    #     time.sleep(speed)
    # win32api.SetCursorPos((x,y1))
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y1,0,0)
    # time.sleep(8) # wait for scroll to finish
    # try pg.moveTo(x, y, TEMPO)
    # # pg.scroll(amount)


def esc():
    print("esc")
    click((5, 100))
    keyboard.press_and_release('esc')
    if(findImage(images["exit"], areas["exitArea"])):
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

    click(points["wave"])
    time.sleep(1)
    start()


def start():
    print("start")

    global runType
    level = None

    if(runType == "gold"):
        level = points["jrh"]
    elif(runType == "kn5"):
        level = points["kn"]

    click(level)
    time.sleep(2.5)
    click(points["go"])


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
    # print("main")
    # start()
    # loop()
    setFormation(formations["main"])
    # scrollDown()


main()