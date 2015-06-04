from collections import OrderedDict
from pprint import pprint
from random import sample, randint

TITLE = "== Candle =="
INTRO = "You find yourself all alone in the beautiful but exceedingly creepy old mansion \nwith nothing but a candle for company. " \
        "The tiny flame is barely enough to push back \nthe dark but you think that your eyes are adjusting."
PROMPT = "What would you like to do? \n>"
rooms = OrderedDict()
rooms['Entry'] = "You are standing in the grand entrance of the mansion."
rooms['Parlor'] = "You find yourself standing in a small parlor, decorated in pinks and purples."
rooms['Dining Room'] = "This is the largest dining room you've ever seen. " \
                       "You imagine an entire army could feast at that table."
rooms['Library'] = "This room is full of books and curios. Its a shame so many of them are covered in blood."
rooms['Ballroom'] = "You find yourself in an imposing ballroom. The silence practically echoes here."
rooms['Gallery'] = "It seems to be a gallery of family portraits. Oil paintings of someone's creepy dead " \
                   "relatives line the walls."
rooms['Sunroom'] = "This room would be beautiful and full of sun during the day, but right now it is " \
                   "creepy by moonlight."
rooms['Smoking room'] = "This room smells disgustingly of old cigars. You imagine it was a smoking room."
DIRECTIONS = ['North', 'South', 'East', 'West', 'N', 'S', 'E', 'W']



class Room:
    name = ""
    description = ""
    exits = None
    discovered = False

    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.exits = {}

    def __str__(self):
        return self.description

    def connect(self, room, direction):
        self.exits[direction] = room
        if direction == "North":
            opposite_direction = "South"
        elif direction == "South":
            opposite_direction = "North"
        elif direction == "East":
            opposite_direction = "West"
        elif direction == "West":
            opposite_direction = "East"
        else:
            raise ValueError('invalid direction')
        room.exits[opposite_direction] = self


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
        self.is_running = True

    def _stop(self):
        self.is_running = False

    def parse_user_action(self, user_input):
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
            print("You move to the " + user_input + ".")
            self.move(user_input)
        elif user_input in ["Look", "L"]:
            self.current_location.discovered = False
            self.get_status()
        elif user_input in ["Map", "M"]:
            self.print_map()
        elif user_input == "Exit":
            self.is_running = False
        else:
            print("sorry, there is no such action")

    def get_status(self):
        if self.current_location.discovered == True:
            pass
        else:
            self.current_location.discovered = True
            print(self.current_location)
        for direction in self.current_location.exits.keys():
            print("There is an exit to the " + direction + ".")

    def move(self, direction):
        try:
            self.current_location = self.current_location.exits[direction]
        except:
            raise ValueError('invalid direction')

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
        room_width = max([len(r.name) for r in self.rooms])
        map = []
        for y in reversed(range(-6, 7)):
            row = []
            for x in range(-6, 7):
                room = self.coordinate_map.get((x, y), Room(' ' * room_width))
                if room.discovered:
                    row.append(room.name)
                else:
                    row.append(' ' * room_width)
            print(row)
            map.append(row)

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

# TODO:
#   * prettier map
#   * add prettier UI elements
#   * connections between rooms
# TODO: add items to game
if __name__ == "__main__":
    ir = [Room(name, desc) for name, desc in rooms.items()]
    game = Game(ir)

    print(TITLE)
    print("")
    print(INTRO)
    print("")
    while game.is_running:
        game.get_status()
        user_input = input(PROMPT)
        game.parse_user_action(user_input)
        print("\n \n")
