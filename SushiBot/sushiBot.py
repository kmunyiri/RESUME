# sushiBot.py - bot that is used for playing sushi game using GUI automation

# Link to the game which this code was tested on
import random
from collections import OrderedDict
import time
import pyautogui  # used for gui automation
url = "https://www.gamenora.com/game/sushi-go-round/# "


ingredients = {"shrimp": 5, "rice": 10,
               "nori": 10, "roe": 10, "salmon": 5, "unagi": 5}

min = 4


def gameIntro(s):
    """ Goes throught the motions of getting to the game one page loaded"""
    print("INTRO")
    skip = s

    for i in range(4):
        pyautogui.press("down")

    # Make full screen
    pyautogui.moveTo(940, 770, duration=0.25)
    pyautogui.doubleClick()

    # Click play
    pyautogui.moveTo(640, 500, duration=1)
    pyautogui.doubleClick()

    time.sleep(7)

    # Click play
    pyautogui.moveTo(630, 350, duration=1)
    pyautogui.doubleClick()

    # Click continue
    pyautogui.moveTo(640, 660, duration=1)
    pyautogui.doubleClick()

    if skip == 1:
        pyautogui.moveTo(1080, 760, duration=1)
        pyautogui.doubleClick()

    # Click continue
    pyautogui.moveTo(640, 640, duration=1)
    pyautogui.doubleClick()


def getIngredient(food):
    """ Given ingredient it will carry out the instructions to use that ingredient in the game and update the dictionary """
    if ingredients[food] > 0:
        # instructions to click rice
        if food == "rice":
            pyautogui.moveTo(260, 560, duration=0.6)
            pyautogui.click()
            # after ingredient is used remove it from dictionary
            ingredients["rice"] = ingredients["rice"] - 1
        # instructions to click nori
        elif food == "nori":
            pyautogui.moveTo(178, 646, duration=0.6)
            pyautogui.click()
            ingredients["nori"] = ingredients["nori"] - 1
        # instructions to click roe
        elif food == "roe":
            pyautogui.moveTo(260, 646, duration=0.6)
            pyautogui.click()
            ingredients["roe"] = ingredients["roe"] - 1
        # instructions to click salmon
        elif food == "salmon":
            pyautogui.moveTo(170, 745, duration=0.6)
            pyautogui.click()
            ingredients["salmon"] = ingredients["salmon"] - 1

    else:
        restockIngredient(food)
        time.sleep(7)  # wait for food to load before you try again
        getIngredient(food)


def restockIngredient(food):
    """Given an ingredient it will carry out the instructions """
    # instructions to click rice
    if food == "rice":
        pyautogui.moveTo(1040, 600, duration=0.25)  # click phone
        pyautogui.click()
        pyautogui.moveTo(956, 489, duration=0.25)  # rice
        pyautogui.click()
        pyautogui.moveTo(1015, 468, duration=0.25)  # buy rice
        pyautogui.click()
        pyautogui.moveTo(915, 490, duration=0.25)
        pyautogui.click()
        ingredients["rice"] = ingredients["rice"] + 10
    # instructions to click nori
    elif food == "nori":
        pyautogui.moveTo(1040, 600, duration=0.25)  # click phone
        pyautogui.click()
        pyautogui.moveTo(961, 457, duration=0.25)  # toppings
        pyautogui.click()
        pyautogui.moveTo(930, 461, duration=0.25)  # buy nori
        pyautogui.click()
        pyautogui.moveTo(915, 490, duration=0.25)
        pyautogui.click()
        ingredients["nori"] = ingredients["nori"] + 10
    # instructions to click roe
    elif food == "roe":
        pyautogui.moveTo(1040, 600, duration=0.25)  # click phone
        pyautogui.click()
        pyautogui.moveTo(961, 457, duration=0.25)  # toppings
        pyautogui.click()
        pyautogui.moveTo(1058, 461, duration=0.25)  # buy roe
        pyautogui.click()
        pyautogui.moveTo(915, 490, duration=0.25)
        pyautogui.click()
        ingredients["roe"] = ingredients["roe"] + 10

    elif food == "salmon":
        pyautogui.moveTo(1040, 600, duration=0.25)  # click phone
        pyautogui.click()
        pyautogui.moveTo(961, 457, duration=0.25)  # toppings
        pyautogui.click()
        pyautogui.moveTo(930, 560, duration=0.25)  # buy salmon
        pyautogui.click()
        pyautogui.moveTo(915, 490, duration=0.25)
        pyautogui.click()
        ingredients["salmon"] = ingredients["salmon"] + 5


def clearTable():
    """Carries out instructions to clear the table after customers are done eating"""
    for i in range(6):
        pyautogui.moveTo()
        pyautogui.click(230 + (170 * i), 340)


def makeSushi(type, amount):
    """Given the type of sushi and the amount, carries out instruction to fulfill order"""
    # onigiri, california roll, maki
    recipe = [["rice", "rice", "nori"], ["rice", "nori", "roe"], ["rice", "nori", "roe", "roe"],
              ["rice", "nori", "salmon", "salmon"]]
    clearTable()
    if type == "onigiri" and amount > 0:
        for i in range(amount):
            print(f"making onigiri\n")
            ing = recipe[0]

            # instructions for making onigiri
            for food in ing:
                getIngredient(food)
            pyautogui.moveTo(450, 654, duration=0.5)  # click mat
            pyautogui.click()

    elif type == "california roll" and amount > 0:
        for i in range(amount):
            print(f"making california roll\n")

            # instructions for making a california roll
            ing = recipe[1]

            for food in ing:
                getIngredient(food)
            pyautogui.moveTo(450, 654, duration=0.5)  # click mat
            pyautogui.click()

    elif type == "maki" and amount > 0:
        for i in range(amount):
            print(f"making maki\n")

            ing = recipe[2]

            # instructions for making maki
            for food in ing:
                getIngredient(food)
            pyautogui.moveTo(450, 654, duration=0.5)  # click mat
            pyautogui.click()

    elif type == "salmon" and amount > 0:
        for i in range(amount):
            print("making salmon\n")
            ing = recipe[3]

            for food in ing:
                getIngredient(food)
            pyautogui.moveTo(450, 654, duration=0.5)  # click mat
            pyautogui.click()


def makeSushi2(order):
    """Takes a list of orders and fulfill thems using makeSushi"""
    for key in order:
        print(f"Make order for {key}...")
        makeSushi(order[key], 1)
    print("Done with batch")


# orders gives list of box tuples
def orderHelp(orders, name):
    """Given a list of orders and a customer it will return a dictionary that associates the order with a position"""
    dict = {}
    for order in orders:
        dict[order.left] = name
    return dict


def orderOrders(orders1, orders2, orders3, orders4):
    """ Given orders returns ordered dictinoary of customers and their orders using the range """
    dict = {}

    cOrders = orderHelp(orders1, "onigiri") | orderHelp(orders2, "california roll") | orderHelp(orders3,
                                                                                                "maki") | orderHelp(
        orders4, "salmon")

    for key in cOrders:

        if int(key) > 90 and int(key) < 275:
            dict["customer 1"] = cOrders[key]

        elif int(key) > 290 and int(key) < 440:
            dict["customer 2"] = cOrders[key]

        elif int(key) > 460 and int(key) < 610:
            dict["customer 3"] = cOrders[key]

        elif int(key) > 630 and int(key) < 780:
            dict["customer 4"] = cOrders[key]

        elif int(key) > 800 and int(key) < 950:
            dict["customer 5"] = cOrders[key]

        elif int(key) > 980 and int(key) < 1120:
            dict["customer 6"] = cOrders[key]

    return OrderedDict(sorted(dict.items()))


def checkRemakes(new, old):
    """Checks if any orders need to be remade"""
    remake = {}
    if old == {}:
        return new
    for k in new:
        if k in old.keys() and new[k] == old[k]:
            remake[k] = new[k]
            del old[k]
    return remake | old


time.sleep(3)  # gives user time to move to appropriate screen
skip = 1


# Intro
gameIntro(1)

old = {}
while True:
    im = pyautogui.screenshot()

    sushis = list(pyautogui.locateAllOnScreen("onigiri.png", confidence=0.925))
    sushis2 = list(pyautogui.locateAllOnScreen(
        "californiaRoll.png", confidence=0.94))
    sushis3 = list(pyautogui.locateAllOnScreen(
        "makiRoll.png", confidence=0.98))
    sushis4 = list(pyautogui.locateAllOnScreen(
        "salmonRoll.png", confidence=0.96))

    orders = orderOrders(sushis, sushis2, sushis3, sushis4)

    # orders = checkRemakes(new, old)

    print(orders)
    makeSushi2(orders)

    time.sleep(5)
    clearTable()

    # order any ingredients that are below the minimum amount
    for ingredient, amount in ingredients.items():
        if amount < min:
            restockIngredient(ingredient)
