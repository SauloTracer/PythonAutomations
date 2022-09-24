''' Boiler plate for relative path import'''
# Add's the project root folder to the path so we can import the Auto module normally
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
#########################################################

from Auto import *
import time

# Identify best filter to select a monster
# Extract text from screen area (Tesseract)
# Identify how much is needed to buy a specific upgrade
UPDATE_TIME = 0.5
WATCH_ADS = False
RUN_TYPE = "kn5"
# RUN_TYPE = "gold"

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
    ],
    "new": [
        "kevin", "speedy", "neko"
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
    drag((1180,930), (1180, 500), 7)
    # print("scrollDown finished")


def CheckForExit():
    if(findImage(images["exit"], areas["exitArea"], tries=5)):
        esc((5,100))


def buy(point):
    print("buy")
    click(point)
    time.sleep(1)
    esc((5,100))
        

def restart():
    print("restart")
    click(points["wave"])
    time.sleep(1)
    start()


def start():
    print("start")

    global RUN_TYPE
    level = None

    if(RUN_TYPE == "gold"):
        level = points["jrh"]
    elif(RUN_TYPE == "kn5"):
        level = points["kn"]

    click(level)
    time.sleep(2.5)
    click(points["go"])


def loop():
    print("loop")

    global RUN_TYPE
    global UPDATE_TIME

    while True:
        if keyboard.is_pressed("q"):
            break

        if(point := findImage(images["ad"], areas["center"])):
            time.sleep(1)
            if WATCH_ADS:
                click(point)
                time.sleep(5)
                CloseAd()
                time.sleep(2)
            esc((5,100))

        if(point := findImage(images["coin"], areas["center"])):
            time.sleep(1)
            buy(point)
            if(RUN_TYPE == "kn5"):
                time.sleep(4)
                restart()
        
        if(point := findImage(images["continue"], areas["dc"])):
            time.sleep(1)
            click(point)
            time.sleep(2)
            start()

        CheckForExit()
        
        time.sleep(UPDATE_TIME)


def main():
    start()
    loop()


main()