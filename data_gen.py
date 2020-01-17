# SETTINGS
MAX_SHIP_SIZE = 5
MIN_SHIP_SIZE = 1
MAX_SHIP_AMOUNT = 25
MAP_WID = 10 # map x
MAP_LEN = 10 # map y
DESIRED_STATES = 0 # states to generate

#-------------------------------------#

import pprint
from random import randint

# start generating test cases

def manhattan_dist(x1, y1, x2, y2):
    return (abs(x1 - x2) + abs(y1 - y2)) == 1

def generate_state(MAX_SHIP_SIZE, MIN_SHIP_SIZE, MAX_SHIP_AMOUNT, MAP_WID, MAP_LEN):
    ship_locs = set()
    blocked = set()

    ship_values = []
    ship_amount = randint(1, MAX_SHIP_AMOUNT)
    ship_amount_test = ship_amount
    while ship_amount > 0:
        ship_len = randint(MIN_SHIP_SIZE, min(MAX_SHIP_SIZE, ship_amount))
        ship_amount -= ship_len
        ship_values.append(ship_len)

    ship_values_test = ship_values.copy()
    print("---------")
    print("GENERATED STATE")
    print("Ship amount: {}".format(ship_amount_test))
    print("Ship values: {}".format(ship_values))

    # insert all generated ships

    confirmed_ships = []

    while ship_values:
        ship = ship_values.pop()
        # direction check
        horizontal = bool(randint(0, 1))

        print("Attempting to insert ship with length {}".format(ship))
        print("Horizontal: {}".format(horizontal))

        x = randint(0, MAP_WID - 1)
        y = randint(0, MAP_LEN - 1)

        # checking if we can place it there

        if horizontal:
            failed_to_place = 0
            for length in range(0, ship):
                if (x + length, y) in blocked or x + length > MAP_WID - 1:
                    failed_to_place = 1
                    break
                for block in blocked:
                    if manhattan_dist(block[0], block[1], x + length, y):
                        failed_to_place = 1
                        break
                if failed_to_place == 1:
                    break
            if failed_to_place == 1:
                continue
            # we have a successful placement!
            for length in range(0, ship):
                blocked.add((x + length, y))
                blocked.add((x + length - 1, y))
                blocked.add((x + length + 1, y))
                blocked.add((x + length, y + 1))
                blocked.add((x + length, y - 1))

                ship_locs.add((x + length, y))
            confirmed_ships.append(ship)

        else:
            failed_to_place = 0
            for length in range(0, ship):
                if (x, y + length) in blocked or y + length > MAP_LEN - 1:
                    failed_to_place = 1
                    break
                for block in blocked:
                    if manhattan_dist(block[0], block[1], x, y + length):
                        failed_to_place = 1
                        break
                if failed_to_place == 1:
                    break
            if failed_to_place == 1:
                continue
            # we have a successful placement!
            for length in range(0, ship):
                blocked.add((x, y + length))
                blocked.add((x, y + length - 1))
                blocked.add((x, y + length + 1))
                blocked.add((x + 1, y + length))
                blocked.add((x - 1, y + length))

                ship_locs.add((x, y + length))
            confirmed_ships.append(ship)

    print("---------")
    print("Final state data:")
    print("Planned amount of ship values: {}".format(ship_values_test))
    print("Actual amount of ship values: {}".format(confirmed_ships))

    base = [[0 for i in range(MAP_WID)] for j in range(MAP_LEN)]

    #for loc in ship_locs:
     #   base[loc[0]][loc[1]] = "0"
    for i in range(randint(20, 50)):
        x = randint(0, 9)
        y = randint(0, 9)
        if (x, y) and (y, x) not in ship_locs:
            base[x][y] = "O"

    if len(confirmed_ships) == 0:
        return generate_state(MAX_SHIP_SIZE, MIN_SHIP_SIZE, MAX_SHIP_AMOUNT, MAP_WID, MAP_LEN)
    return base, ship_locs, confirmed_ships

# generate board states to learn from, write states to CSV

import csv
generated_states = 0
csv_file = open("data.csv", "w", newline="")
csv_writer = csv.writer(csv_file, delimiter=",")

# add columns to our data file
csv_writer.writerow(["grid", "ship locations"])

while generated_states != DESIRED_STATES:
    base, ship_locs, confirmed_ships = generate_state(MAX_SHIP_SIZE, MIN_SHIP_SIZE, MAX_SHIP_AMOUNT, MAP_WID, MAP_LEN)
    csv_writer.writerow([generated_states, list(ship_locs), base])
    generated_states += 1
