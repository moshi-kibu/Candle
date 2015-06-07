from collections import OrderedDict
from random import sample

from models import Room

DIRECTIONS = ['North', 'South', 'East', 'West', 'N', 'S', 'E', 'W']


def _choose_random_direction():
    # a randomized direction strategy
    # interface is:
    #   takes no parameters
    #   returns one of the strings ("North", "South", "East", or "West")
    return sample(["North", "South", "East", "West"], 1)[0]


class Game:
    current_location = None
    rooms = []
    is_running = False
    coordinate_map = None
    current_coordinate = (0, 0)

    def __init__(self, rooms, direction_strategy=_choose_random_direction):
        self.rooms = rooms
        self.current_location = rooms[0]

        # needed to prevent first room from being self-connected
        self.coordinate_map = {(0, 0): self.current_location}

        self.make_map(direction_strategy)
        self.current_location = rooms[0]
        self.current_status = self.current_location.describe()
        self.current_location.is_discovered = True
        self.is_running = True

    def _stop(self):
        self.is_running = False

    def respond_to_user_input(self, user_input):
        user_input = user_input.capitalize()
        if user_input in DIRECTIONS:
            if user_input == "N":
                user_input = "North"
            elif user_input == "S":
                user_input = "South"
            elif user_input == "E":
                user_input = "East"
            elif user_input == "W":
                user_input = "West"
            self.move(user_input)
        elif user_input in ["Look", "L"]:
            self.current_location.is_discovered = False
            self.current_status = self.current_location.describe()
        elif user_input in ["Map", "M"]:
            self.print_map()
        elif user_input == "Exit":
            self.is_running = False
        else:
            print("sorry, there is no such action")

    def move(self, direction):
        try:
            self.current_status = "You move to the " + direction + ".\n"
            self.current_location = self.current_location.exits[direction]
            self.current_status += self.current_location.describe()
            self.current_location.is_discovered = True
        except KeyError:  # no exit this way
            self.current_status = "There's no exit that way, dorkface."

    def make_map(self, direction_strategy):
        rooms = self.rooms[1:]
        current_coordinate = (0, 0)

        while len(rooms) != 0:
            room = rooms[0]
            direction = direction_strategy()
            coordinates = self._shift_coordinates(current_coordinate, direction)
            if coordinates in self.coordinate_map:
                # connect current room to existing room; don't throw away new room
                self.current_location.connect(self.coordinate_map[coordinates], direction)
            else:
                # connect current room to room in loop, adds new room to map, moves to room
                self.coordinate_map[coordinates] = room
                self.current_location.connect(room, direction)
                self.current_location = self.current_location.exits[direction]
                current_coordinate = coordinates
                del rooms[0]

    def print_map(self):
        # room_width = max([len(r.name) for r in self.rooms])
        top_line = ["|" + ("_" * 20) + ""]
        empty_line = ["|" + (" " * 20) + ""]
        bottom_line = ["|" + ("_" * 20) + ""]
        map = []
        for y in reversed(range(-6, 7)):
            row = []
            for x in range(-6, 7):
                room = self.coordinate_map.get((x, y), Room("weird thing"))
                if room.is_discovered:
                    row.append(room.name_string)
                else:
                    row.append("|" + (" " * 20) + "")
            map.append(row)
        for row in map:
            print("".join(top_line * len(map)))
            print("".join(empty_line * len(map)))
            print("".join(row))
            # print("".join(bottom_line * len(map)))

    def _shift_coordinates(self, current_coordinate, direction):
        if direction == "North":
            coordinates = (current_coordinate[0], current_coordinate[1] + 1)
        elif direction == "South":
            coordinates = (current_coordinate[0], current_coordinate[1] - 1)
        elif direction == "East":
            coordinates = (current_coordinate[0] + 1, current_coordinate[1])
        else:
            coordinates = (current_coordinate[0] - 1, current_coordinate[1])
        return coordinates
