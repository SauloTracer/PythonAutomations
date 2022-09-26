''' Boiler plate for relative path import'''
# Add's the project root folder to the path so we can import the Auto module normally
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
#########################################################

from Auto import *
import time

# Extract text from screen area (Tesseract)
# Identify how much is needed to buy a specific upgrade
# If not enough gems or gold, run jrh to get more and retry

UPDATE_TIME = 0.5
REMOVE_OFFSET_Y = 80
SCROLL_LIMIT = 50

# WATCH_ADS = True
WATCH_ADS = False

# RUN_TYPE = "kn5"
# RUN_TYPE = "gold"
RUN_TYPE = "blueTokens"


areas = {
    "tr": (1090, 30, 106, 80),
    "center": (700, 500, 500, 150),
    "dc": (800, 720, 300, 100),
    "formation": (796, 325, 327, 386),
    "monsterSelection": (735, 195, 80, 775),
    "exitArea": (917, 298, 81, 39),
    "sorts": (715, 145, 370, 55),
    "monsterName": (840, 770, 250, 40),
    "screenTitle": (715, 95, 300, 60),
}

points = {
    "kn": (812, 363),       # king normal
    "jrh": (962, 724),      # joint revenge hard
    "esn": (839,922),       # evil summoner normal
    "go": (959, 978),       # Confirm formation
    "wave": (1142, 68),     # Wave
    "pos1": (846, 260),     # Position 1
    "pos2": (965, 263),     # Position 2
    "pos3": (1079, 262),    # Position 3
    "pos4": (846, 435),     # Position 4
    "pos5": (965, 435),     # Position 5
    "pos6": (1077, 435),    # Position 6
    "pos7": (846, 610),     # Position 7
    "pos8": (965, 610),     # Position 8
    "pos9": (1077, 610),    # Position 9
    "level": (774,172),     # Level sort button
    "rarity": (894, 172),   # Rarity sort button
    "speed": (1014, 172),   # Speed sort button
    "closeMonsterInfo": (1170, 1000), # Close monster info
}

images = {
    "coin": "img/coin.png",
    "ad": "img/ad.png",
    "continue": "img/continue.png",
    "exit": "img/exit.png",
    "ok": "img/ok.png",
    "classic": "img/classic.png",
    "remove": "img/remove.png",
    "emptyPos": "img/emptyPos.png",
    "select": "img/select.png",
    "challenge": "img/challenge.png",
    "selectMap": "img/selectMap.png",
    "recharge": "img/recharge.png",
    "normal": "img/normal.png",
    "confirm": "img/confirm.png",
}

sorts = {
    "lowLevel": ("img/lowLevel.png", points["level"]),
    "highLevel": ("img/highLevel.png", points["level"]),
    "fast": ("img/fast.png", points["speed"]),
    "slow": ("img/slow.png", points["speed"]),
    "rare": ("img/rare.png", points["rarity"]),
    "common": ("img/common.png", points["rarity"]),
}

monsters = {
    "speedy": ("img/speedy.png", "img/speedyName.png", sorts["slow"]),
    "kevin": ("img/kevin.png", "img/kevinName.png", sorts["highLevel"]),
    "neko": ("img/neko.png", "img/nekoName.png", sorts["slow"]),
    "volt": ("img/volt.png", "img/voltName.png", sorts["fast"]),
    "deathByte": ("img/deathByte.png", "img/deathByteName.png", sorts["highLevel"]),
    "kingSlime": ("img/kingSlime.png", "img/kingSlimeName.png", sorts["highLevel"]),
    "kingsLover": ("img/kingsLover.png", "img/kingsLoverName.png", sorts["lowLevel"]),
    "crispy": ("img/crispy.png", "img/crispyName.png", sorts["rare"]),
    "felina": ("img/felina.png", "img/felinaName.png", sorts["highLevel"]),
    "hellHound": ("img/hellHound.png", "img/hellHoundName.png", sorts["rare"]),
    "ra": ("img/ra.png", "img/raName.png", sorts["rare"]),
    "icy": ("img/icy.png", "img/icyName.png", sorts["highLevel"]),
    "iceDragon": ("img/iceDragon.png", "img/iceDragonName.png", sorts["highLevel"]),
    "iceAngel": ("img/iceAngel.png", "img/iceAngelName.png", sorts["rare"]),
}

formations = {
    "main": [
        "neko", "kevin", "speedy", 
        "volt", "deathByte", "kingSlime", 
        "crispy", "felina", "hellHound"
    ],
    "new": [
        "kevin", "speedy", "volt",
        "crispy", "ra", "kingSlime",
        "hellHound", "felina", "neko"
    ]
}


def sortBy(sort):
    if findImage(sort[0], areas["sorts"]):
        return
    while not findImage(sort[0], areas["sorts"], tries=3):
        click(sort[1])
        time.sleep(3)


def setMonster(monster, position):
    if not isPositionEmpty(position):
        click(position)
        time.sleep(3)
        res = findImage(monster[1], areas["monsterName"], tries=3)
        if res:
            print("Monster already in position")
            return
        else:
            print("Clearing position")
            clearPosition(position)
    
    print("Entering selection screen")
    while not findImage(images["select"], areas["screenTitle"]):
        click(position)
        time.sleep(5)

    print("Sorting by", monster[2][0])
    sortBy(monster[2])

    time.sleep(3)

    print("Searching for monster")
    while not (point := findImage(monster[0], areas["monsterSelection"], tries=3)):
        scrollDown()
    if point:
        print("Found monster")
        click(point)


def setFormation(formation):
    print("Setting formation: ", formation)
    for i in range(len(formation)):
        print(formation[i])
        setMonster(monsters[formation[i]], points["pos"+str(i + 1)])
    time.sleep(5)
    click(points["closeMonsterInfo"])


def clearPosition(position):
    x, y = position
    y += REMOVE_OFFSET_Y
    while not isPositionEmpty(position):
        click((x, y))
        time.sleep(.5)


def isPositionEmpty(position):
    res = findImage(images["emptyPos"], areaFromPoint(position, 40, 60))
    if res:
        print("Position is empty")
    else:
        print("Position is occupied")
    return res


def clearFormation():
    while point := findImage(images["remove"], areas["formation"]):
        click(point)
        time.sleep(1)


def scrollDown():
    print("Scrolling down")
    drag((1180,930), (1180, 500), 10)
    # print("scrollDown finished")


def checkForExit():
    if(findImage(images["exit"], areas["exitArea"], tries=5)):
        esc((5,100))


def buy(point):
    print("buy")
    click(point)
    if waitForImage(images["ok"], None):
        esc((5,100))
        

def resetLevel():
    print("reset level")
    click(points["wave"])
    if(waitForImage(images["classic"], None)):
        start()


def restart():
    targetImage = images["continue"]
    targetImageArea = areas["dc"]
    checkImage = images["classic"]

    if (RUN_TYPE == "blueTokens"):
        targetImage = images["selectMap"]
        targetImageArea = None

    if(point := findImage(targetImage, targetImageArea)):
        click(point)
        waitForImage(checkImage, None)
        start()


def start():
    print("start")

    global RUN_TYPE
    level = None

    if(RUN_TYPE == "gold"):
        level = points["jrh"]
    elif(RUN_TYPE == "kn5"):
        level = points["kn"]
    elif(RUN_TYPE == "blueTokens"):
        clickImage(images["challenge"], None)
        time.sleep(3)
        level = points["esn"]

    click(level)
    
    if (RUN_TYPE == "blueTokens"):
        time.sleep(3)
        if point := findImage(images["recharge"], None):
            click(point)
            waitForImage(images["normal"], None)
            click(level)
            waitForImage(images["confirm"], None)
        setFormation(formations["new"])
        time.sleep(3)

    waitForImage(images["confirm"], None)
    click(points["go"])


def ad():
    if(point := findImage(images["ad"], areas["center"])):
        print("Ad")
        time.sleep(1)
        if WATCH_ADS:
            click(point)
            print("Watching ad")
            time.sleep(5)
            print("Closing ad")
            closeAd(images["ok"])
            if waitForImage(images["ok"], None):
                esc((5,100))
        else:
            print("Escaping ad")
            esc((5,100))


def vendor():
    if(point := findImage(images["coin"], areas["center"])):
        buy(point)
        if(RUN_TYPE == "kn5"):
            while findImage(images["ok"], None):
                time.sleep(1)
            resetLevel()


def loop():
    print("loop")

    global RUN_TYPE
    global UPDATE_TIME

    while True:
        if keyboard.is_pressed("q"):
            break

        ad()
        vendor()
        checkForExit()
        restart()

        time.sleep(UPDATE_TIME)


def main():
    start()
    loop()


main()