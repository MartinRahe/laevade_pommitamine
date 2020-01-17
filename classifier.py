import csv
import numpy as np


class Feature:
    def __init__(self):
        self.no_ship = {"0": 1, "O": 1, "x": 1, "X": 1, "OOB": 1}
        self.ship = {"0": 1, "O": 1, "x": 1, "X": 1, "OOB": 1}

    def __str__(self):
        return "No_ship: " + str(self.no_ship) + "\n" + "Ship: " + str(self.ship)

    def sum(self, array):
        if array == "no_ship":
            return sum(self.no_ship.values())
        elif array == "ship":
            return sum(self.ship.values())



class NaiveBayesGuesser:
    def __init__(self, laud, data="data.csv"):
        self.grid = laud
        self.guessed = set()
        file_handle = open(data)
        csv_handle = csv.reader(file_handle, delimiter=",")
        training_data = []
        training_grid = []
        i = 0
        for row in csv_handle:
            try:
                i += 1
                training_data.append(eval(row[1]))
                training_grid.append(eval(row[2]))
            except:
                pass
        #flat_list = []
        #for sublist in training_data:
        #    for item in sublist:
        #        flat_list.append(item)
        #training_data = flat_list
        #training_data = training_data[1:]
        #training_data = []

        self.features = self.train(training_grid, training_data, i)
        #print(self.features)

    def get_surroundings(self, point):
        x = int(point[0])
        y = int(point[1])
        return [(x-1, y+1), (x, y+1), (x+1, y+1),
                                (x-1, y)              , (x+1, y),
                                (x-1, y-1), (x, y-1), (x+1, y-1)]


    def remove_oob(self, points):
        clean_list = []
        for point in points:
            if 9 >= point[0] >= 0:
                if 9 >= point[1] >= 0:
                    clean_list.append(point)
        return clean_list


    def train(self, training_grid, training_data, lines_of_data):
        """
        :type training_data: list
        :type training_grid: list
        :type lines_of_data: int
        """
        features = {"NW": Feature(), "N": Feature(), "NE": Feature(),
                    "E": Feature(), "W": Feature(),
                    "SW": Feature(), "S": Feature(), "SE": Feature()}

        for i in range(lines_of_data - 1):
            grid = training_grid[i]
            for ship_point in training_data[i]:
                neighbours = self.get_surroundings(ship_point)
                inbounds_neighbours = self.remove_oob(neighbours)
                # start iterating through features, increasing values where needed
                for index, feature in enumerate(features):
                    if neighbours[index] not in inbounds_neighbours:
                        features[feature].ship["OOB"] += 1
                        continue
                    neighbour_value = str(grid[neighbours[index][0]][neighbours[index][1]])
                    features[feature].ship[neighbour_value] += 1
        return features

    def get_guess(self, grid, enemy_grid):
        """

        :type guessed: set
        """
        max_guess = None
        max_prob = np.NINF

        positions = [(x, y) for y in range(10) for x in range(10)]
        for pos in positions:
            neighbours = self.get_surroundings(pos)
            clean_neighbours = self.remove_oob(neighbours)
            current_prob = 0
            for index, feature in enumerate(self.features):
                #if neighbours[index] not in clean_neighbours:
                #    neighbour_value = "OOB"
                try:
                    neighbour_value = str(grid[neighbours[index][1]][neighbours[index][0]])
                except:
                    neighbour_value = "OOB"

                count_of_neighbour_value = self.features[feature].ship[neighbour_value]
                count_of_no_ship_neighbour_value = self.features[feature].no_ship[neighbour_value]
                count_of_all_neighbour_value = self.features[feature].no_ship[neighbour_value] + count_of_neighbour_value
                count_of_yes = self.features[feature].sum("ship")
                count_all = self.features[feature].sum("no_ship") + count_of_yes

                prob = np.log((count_of_neighbour_value / count_of_yes) * (count_of_yes / count_all) / (count_of_all_neighbour_value / count_all))
                #print(prob)
                current_prob += prob
            if current_prob > max_prob and pos not in self.guessed:
                max_guess = pos
                max_prob = current_prob
        print(max_prob, max_guess)
        self.guessed.add(max_guess)
        return max_guess

    def guess_feedback(self, point, grid, hit):
        neighbours = self.get_surroundings(point)
        clean_neighbours = self.remove_oob(neighbours)
        for index, feature in self.features:
            value = self.get_pos(grid, neighbours[index])
            if hit:
                self.features[feature].ship[value] += 1
            else:
                self.features[feature].no_ship[value] += 1

    def get_pos(self, grid, pos):
        try:
            return str(grid[pos[1]][pos[0]])
        except:
            return "OOB"


base = [["0" for i in range(10)] for j in range(10)]
nbg = NaiveBayesGuesser(base)
print(nbg.get_guess(base))
print(nbg.get_guess(base))
print(nbg.get_guess(base))
print(nbg.get_guess(base))
print(nbg.get_guess(base))
print(nbg.get_guess(base))

