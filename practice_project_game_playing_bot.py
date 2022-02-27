# practice_project_game_playing_bot_tutorial.py - Program automatically plays Sushi
# Go Round game online one game at a time. Some manual adjustments to the code are
# still required, for example when the "game day" changes.

# game URL
# https://www.miniclip.com/games/sushi-go-round/en/

# Tutorial used for help
# https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117

# NOTES: The positions of buttons have been defined so that page cookies have been accepted
# and then nothing has been moved on the screen.
# Tested with screen resolution 1920 x 1080 and Firefox browser.
#
# The game time seems to be
# Day 1: 3 min
# Day 2: 4 min
# Day 3: 5 min
# Day 4: 6 min
# Day ...
# TODO: Add some image recognitition to recognize the Day 1, 2, ..., or manual counter

# Usage in Linux:   python3 [program name].py


import pyautogui as pg
import time


game_time = {
        1: 180,
        2: 240,
        3: 300,
        4: 360
        }

day_number = 4


# Food items with the starting amounts
food_items = {
        "shrimp": 5,
        "rice" : 10,
        "nori" : 10,
        "roe" : 10,
        "salmon" : 5,
        "unagi" : 5
        }



# pg.PAUSE = 1    # Seems to work well with this, but slow
# pg.PAUSE = 0.75
# pg.PAUSE = 0.5    # Seems to make mistakes in some parts


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
    time.sleep(0.5)


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


def remove_empty_plates():
    for i in range(1, 7):
        pg.click(eval("Coor.p_" + str(i)))


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
    if time_elapsed < 60:
        if food_items["rice"] <= 5:
            buy_rice()
        if food_items["salmon"] <= 3:
            buy_salmon()
        elif food_items["shrimp"] <= 3:
            buy_shrimp()
        elif food_items["unagi"] <= 3:
            buy_unagi()
        if food_items["roe"] <= 5:
            buy_roe()
        if food_items["nori"] <= 5:
            buy_nori()
    else:
        if food_items["rice"] <= 5:
            buy_rice()
        if food_items["salmon"] <= 3:
            buy_salmon()
        if food_items["shrimp"] <= 3:
            buy_shrimp()
        if food_items["unagi"] <= 3:
            buy_unagi()
        if food_items["roe"] <= 5:
            buy_roe()
        if food_items["nori"] <= 5:
            buy_nori()
    time.sleep(1.5)


def main():
    pg.PAUSE = 0.2
    # pg.PAUSE = 3.0    # for slowing up clicking to read the text when 
    start_play()    # for first game
    # continue_play()   # for continuing game
    start_time = time.time()
    # After game time no new customers arrive
    while (time.time() - start_time) < (game_time[day_number] + 60):     
        pg.PAUSE = 0.6
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["unagi"] >= 2:
            for _ in list(pg.locateAllOnScreen('sushi_options/unagi_roll.png')):
                make_unagi_roll()            
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["shrimp"] >= 2:
            for _ in list(pg.locateAllOnScreen('sushi_options/shrimp_sushi.png')):
                make_shrimp_sushi()
        pg.PAUSE = 0.2
        remove_empty_plates()
        pg.PAUSE = 0.6
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["salmon"] >= 2:
            for _ in list(pg.locateAllOnScreen('sushi_options/salmon_roll.png')):
                make_salmon_roll()
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["roe"] >= 2:
            for _ in list(pg.locateAllOnScreen('sushi_options/gunkan_maki.png')):
                make_gunkan_maki()
        pg.PAUSE = 0.2
        remove_empty_plates()
        pg.PAUSE = 0.6
        if food_items["rice"] >= 1 and food_items["nori"] >= 1 and food_items["roe"] >= 1:
            for _ in list(pg.locateAllOnScreen('sushi_options/california_roll.png')):
                make_california_roll()
        if food_items["rice"] >= 2 and food_items["nori"] >= 1:
            for _ in list(pg.locateAllOnScreen('sushi_options/onigiri.png')):
                make_onigiri()
        pg.PAUSE = 0.2
        remove_empty_plates()
        if 40 <= (time.time() - start_time) <= game_time[day_number]:
            buy_items(time.time() - start_time)
            remove_empty_plates()


if __name__ == "__main__":
    main()
