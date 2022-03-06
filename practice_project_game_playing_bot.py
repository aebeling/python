# practice_project_game_playing_bot.py - Program automatically plays Sushi
# Go Round game online one game at a time. Some manual adjustments to the code are
# still required, for example when the "game day" changes.

# game URL
# https://www.miniclip.com/games/sushi-go-round/en/

# Tutorial used for help
# https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

# NOTES: The positions of buttons have been defined so that page cookies have been accepted
# and then nothing has been moved on the screen.
# Tested with screen resolution 1920 x 1080 and Firefox browser.

# NOTES related to the game:
# The game times
# Day 1: 3 min
# Day 2: 4 min
# Day 3: 5 min
# Day 4: 6 min
# Day 5: 6 min
# Day ...
#
# Maximum inventories
# Rice, nori, roe 15 items
# Unagi, shrimp, salmon 8 items
# TODO: Add some image recognitition to recognize the Day 1, 2, ..., or counter

# Usage in Linux:   python3 [program name].py


import pyautogui as pg
import time


game_time = {
        1: 180,
        2: 240,
        3: 300,
        4: 360,
        5: 360 
        }

day_number = 3


# Food items in the beginning of each round
food_items = {
        "shrimp": 5,
        "rice" : 10,
        "nori" : 10,
        "roe" : 10,
        "salmon" : 5,
        "unagi" : 5
        }

# Food items with time data of making, added as tuples
cook_time = []

# Belt speed and cash in constants
BELT_CONSTANTS = {
        "speed" : 0.02692998205,    # unit seconds/pixel, about 15 seconds / 557 pixels
        "setup_time" : 9    # 5 s (time of eating) + 4 s (until beginning of conveyor belt)
        }

sushi_prices = {
        "dragon_roll" : 380,
        "unagi_roll" : 320,
        "shrimp_sushi" : 320,
        "salmon_roll" : 280,
        "gunkan_maki" : 120,
        "california_roll" : 80,
        "onigiri" : 60
        }

ingredient_prices = {
        "rice" : 100,
        "unagi" : 350,
        "salmon" : 300,
        "shrimp" : 350,
        "nori" : 100,
        "roe" : 200,    # aka fish egg
        }

money = 0

pauses = {
        "short": 0.2,
        "long": 0.5
        }


class Coor:
    
    # Button coordinates, before game 1
    b_play = (735, 735)   # Play button in the beginning of the game
    b_continue_1_1 = (735, 920)   # Continue button
    b_skip = (1005, 985) # Skip button
    b_continue_1_2 = (735, 930)   # Another continue button

    # Button coordinates, after game 1
    b_continue_2_1 = (740, 901)
    b_continue_2_2 = (738, 968)
    b_yes = (634, 908)
    b_no = (874, 904)
    b_continue_2_3 = (731, 904)
    
    # Food item coordinates
    f_shrimp = (458, 865)   # 11
    f_rice = (512, 865)     # 12
    f_nori = (456, 920)     # 21
    f_roe = (511, 921)      # 22, aka fish_egg
    f_salmon = (459, 980)   # 31
    f_unagi = (513, 975)    # 32

    roll = (622, 917)
    
    # Phone and related coordinates to purchase food items
    phone = (1007, 887)
    hang_up = (1010, 874)

    menu_toppings = (959, 804)
    t_shrimp = (913, 753)
    t_unagi = (997, 757)
    t_nori = (915, 807)
    t_roe = (1002, 806)     # aka fish_egg
    t_salmon = (914, 862)

    menu_rice = (968, 823)
    buy_rice = (965, 811)

    menu_sake = (964, 847)
    buy_sake = (965, 802)

    free_delivery = (911, 820)
    express_delivery = (999, 826)

    # Conveyor belt beginning left edge
    belt_left_edge = (422, 786)

    # Plate coordinates
    p_1 = (500, 733)
    p_2 = (602, 735)
    p_3 = (702, 737)
    p_4 = (805, 738)
    p_5 = (905, 737)
    p_6 = (1008, 738) 



# Starting of the game, at least works in the first time
def start_play():
    pg.click(Coor.b_play)
    pg.click(Coor.b_continue_1_1)
    pg.click(Coor.b_skip)
    pg.click(Coor.b_continue_1_2)

def continue_play():
    pg.click(Coor.b_continue_2_1)
    pg.click(Coor.b_continue_2_2)
    # TODO: Add conditional statement whether user wants to play another game or not
    pg.click(Coor.b_yes)
    # pg.click(Coor.b_no)
    pg.click(Coor.b_continue_2_3)


# Functions to use food items
def use_shrimp():
    pg.click(Coor.f_shrimp)
    food_items["shrimp"] -= 1

def use_rice():
    pg.click(Coor.f_rice)
    food_items["rice"] -= 1

def use_nori():
    pg.click(Coor.f_nori)
    food_items["nori"] -= 1

def use_roe():
    pg.click(Coor.f_roe)
    food_items["roe"] -= 1

def use_salmon():
    pg.click(Coor.f_salmon)
    food_items["salmon"] -= 1

def use_unagi():
    pg.click(Coor.f_unagi)
    food_items["unagi"] -= 1

def roll():
    pg.click(Coor.roll)
    time.sleep(0.8)


# Prepare different sushis
def make_onigiri():
    if food_items["rice"] >= 2 and food_items["nori"] >= 1:
        for _ in range(2):
            use_rice()
        use_nori()
        roll()

def make_california_roll():
    if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["roe"] >= 1:
        use_rice()
        use_nori()
        use_roe()
        roll()

def make_gunkan_maki():
    if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["roe"] >= 2:
        use_rice()
        use_nori()
        for _ in range(2):
            use_roe()
        roll()

def make_salmon_roll():
    if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["salmon"] >= 2:
        use_rice()
        use_nori()
        for _ in range(2):
            use_salmon()
        roll()

def make_shrimp_sushi():
    if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["shrimp"] >= 2:
        use_rice()
        use_nori()
        for _ in range(2):
            use_shrimp()
        roll()

def make_unagi_roll():
    if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["unagi"] >= 2:
        use_rice()
        use_nori()
        for _ in range(2):
            use_unagi()
        roll()

def make_dragon_roll():
    if food_items["rice"] >= 2 and food_items["nori"] >= 1 and food_items["roe"] \
            and food_items["unagi"] >= 2:
                for _ in range(2):
                    use_rice()
                    use_unagi()
                use_nori()
                use_roe()
                roll()


def remove_empty_plates(time_elapsed):
    if time_elapsed > 30:
        for i in range(1, 7):
            pg.click(eval("Coor.p_" + str(i)))


def count_money(time_elapsed):
    global money
    # Reverse iteration to avoid skipping items when deleting
    for i in range(len(cook_time) - 1, -1, -1):
        food = cook_time[i][0]
        time = cook_time[i][1]
        position = cook_time[i][2]
        if (time_elapsed - time) > (
                (position - Coor.belt_left_edge[0]) * BELT_CONSTANTS["speed"]
                + BELT_CONSTANTS["setup_time"]):
            money += sushi_prices[food]
            del cook_time[i]


# Functions to buy food items
def buy_shrimp():
    pg.click(Coor.phone)
    pg.click(Coor.menu_toppings)
    pg.click(Coor.t_shrimp)
    pg.click(Coor.free_delivery)
    food_items["shrimp"] += 5

def buy_rice():
    pg.click(Coor.phone)
    pg.click(Coor.menu_rice)
    pg.click(Coor.buy_rice)
    pg.click(Coor.free_delivery)
    food_items["rice"] += 10

def buy_nori():
    pg.click(Coor.phone)
    pg.click(Coor.menu_toppings)
    pg.click(Coor.t_nori)
    pg.click(Coor.free_delivery)
    food_items["nori"] += 10

def buy_roe():
    pg.click(Coor.phone)
    pg.click(Coor.menu_toppings)
    pg.click(Coor.t_roe)
    pg.click(Coor.free_delivery)
    food_items["roe"] += 10

def buy_salmon():
    pg.click(Coor.phone)
    pg.click(Coor.menu_toppings)
    pg.click(Coor.t_salmon)
    pg.click(Coor.free_delivery)
    food_items["salmon"] += 5

def buy_unagi():
    pg.click(Coor.phone)
    pg.click(Coor.menu_toppings)
    pg.click(Coor.t_unagi)
    pg.click(Coor.free_delivery)
    food_items["unagi"] += 5


def buy_items(time_elapsed):
    global money
    if time_elapsed < game_time[day_number]:
        if food_items["rice"] <= 5 and money >= ingredient_prices["rice"]:
            buy_rice()
            money -= ingredient_prices["rice"]
        if food_items["unagi"] <= 3 and money >= ingredient_prices["unagi"]:
            buy_unagi()
            money -= ingredient_prices["unagi"]
        if food_items["shrimp"] <= 3 and money >= ingredient_prices["shrimp"]:
            buy_shrimp()
            money -= ingredient_prices["shrimp"]
        if food_items["salmon"] <= 3 and money >= ingredient_prices["salmon"]:
            buy_salmon()
            money -= ingredient_prices["salmon"]
        if food_items["roe"] <= 5 and money >= ingredient_prices["roe"]:
            buy_roe()
            money -= ingredient_prices["roe"]
        if food_items["nori"] <= 5 and money >= ingredient_prices["nori"]:
            buy_nori()
            money -= ingredient_prices["nori"]
        time.sleep(2.0)


def main():
    pg.PAUSE = pauses["short"]
    # pg.PAUSE = 3.0
    start_play()    # when starting each day the first time
    # continue_play()   # when trying the same day again as before
    start_time = time.time()
    time.sleep(15)  # Wait a moment for seats to fill

    while (time.time() - start_time) < (game_time[day_number] + 45):
        pg.PAUSE = pauses["short"]

        if food_items["rice"] >= 2 and food_items["nori"] >= 1 and food_items["roe"] >=1 \
                and food_items["unagi"] >= 2 and day_number >= 5:
            for customer_position in list(pg.locateAllOnScreen('sushi_options/dragon_roll.png')):
                make_dragon_roll()
                cook_time.append(("dragon_roll", time.time() - start_time,
                    pg.center(customer_position)[0]))

        if day_number >= 5:
            # pg.PAUSE = pauses["short"]
            remove_empty_plates(time.time() - start_time)

        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["unagi"] >= 2 \
                and day_number >= 4:
            for customer_position in list(pg.locateAllOnScreen('sushi_options/unagi_roll.png')):
                make_unagi_roll()
                cook_time.append(("unagi_roll", time.time() - start_time,
                    pg.center(customer_position)[0]))
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["shrimp"] >= 2 \
                and day_number >= 3:
            for customer_position in list(pg.locateAllOnScreen('sushi_options/shrimp_sushi.png')):
                make_shrimp_sushi()
                cook_time.append(("shrimp_sushi", time.time() - start_time,
                    pg.center(customer_position)[0]))

        if day_number >= 3:
            # pg.PAUSE = pauses["short"]
            remove_empty_plates(time.time() - start_time)

        # pg.PAUSE = pauses["long"]
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["salmon"] >= 2 \
                and day_number >= 2:
            for customer_position in list(pg.locateAllOnScreen('sushi_options/salmon_roll.png')):
                make_salmon_roll()
                cook_time.append(("salmon_roll", time.time() - start_time,
                    pg.center(customer_position)[0]))
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["roe"] >= 2:
            for customer_position in list(pg.locateAllOnScreen('sushi_options/gunkan_maki.png')):
                make_gunkan_maki()
                cook_time.append(("gunkan_maki", time.time() - start_time,
                    pg.center(customer_position)[0]))

        # pg.PAUSE = pauses["short"]
        remove_empty_plates(time.time() - start_time)

        # pg.PAUSE = pauses["long"]
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["roe"] >= 1:
            for customer_position in list(
                    pg.locateAllOnScreen('sushi_options/california_roll.png')):
                make_california_roll()
                cook_time.append(("california_roll", time.time() - start_time,
                    pg.center(customer_position)[0]))
        if food_items["rice"] >= 2 and food_items["nori"] >= 1:
            for customer_position in list(pg.locateAllOnScreen('sushi_options/onigiri.png')):
                make_onigiri()
                cook_time.append(("onigiri", time.time() - start_time,
                    pg.center(customer_position)[0]))

        # pg.PAUSE = pauses["short"]
        count_money(time.time() - start_time)
        buy_items(time.time() - start_time)
        remove_empty_plates(time.time() - start_time)


if __name__ == "__main__":
    main()
