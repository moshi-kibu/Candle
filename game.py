from random import sample
from models import Room, Player

DIRECTIONS = ['North', 'South', 'East', 'West', 'N', 'S', 'E', 'W']

def _choose_random_direction():
    # a randomized direction strategy
    # interface is:
    #   takes no parameters
    #   returns one of the strings ("North", "South", "East", or "West")
    return sample(["North", "South", "East", "West"], 1)[0]


class Game:
    rooms = None
    is_running = False
    coordinate_map = None
    current_coordinate = (0, 0)
    events = None

    def __init__(self, rooms, direction_strategy=_choose_random_direction):
        self.events = []

        self.rooms = rooms
        for room in rooms:
            room.add_receiver(self)

        # needed to prevent first room from being self-connected
        self.coordinate_map = {(0, 0): rooms[0]}
        self.make_map(direction_strategy)
        self.player = Player(rooms[0])
        self.player.add_receiver(self)
        self.is_running = True

    def receive(self, event):
        self.events.append(event)

    def get_status(self):
        status = ""
        for event in self.events:
            status += event.message + "\n"
        self.events = []
        return status

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
            self.player.move(user_input)
        elif user_input in ["Look", "L"]:
            self.player.look()
        elif user_input in ["Map", "M"]:
            self.print_map()
        elif user_input == "Exit":
            self.is_running = False
        else:
            print("sorry, there is no such action")

    def make_map(self, direction_strategy):
        rooms = self.rooms[1:]
        current_coordinate = (0, 0)
        current_location = self.coordinate_map[current_coordinate]

        while len(rooms) != 0:
            room = rooms[0]
            direction = direction_strategy()
            coordinates = self._shift_coordinates(current_coordinate, direction)
            if coordinates in self.coordinate_map:
                # connect current room to existing room; don't throw away new room
                current_location.connect(self.coordinate_map[coordinates], direction)
            else:
                # connect current room to room in loop, adds new room to map, moves to room
                self.coordinate_map[coordinates] = room
                current_location.connect(room, direction)
                current_location = current_location.exits[direction]
                current_coordinate = coordinates
                del rooms[0]

    def print_map(self):
        top_line = ["|" + ("_" * 20) + ""]
        empty_line = ["|" + (" " * 20) + ""]
        room_map = []
        for y in reversed(range(-6, 7)):
            row = []
            for x in range(-6, 7):
                room = self.coordinate_map.get((x, y), Room("weird thing"))
                if room.is_discovered:
                    row.append(room.name_string)
                else:
                    row.append("|" + (" " * 20) + "")
            room_map.append(row)
        for row in room_map:
            print("".join(top_line * len(room_map)))
            print("".join(empty_line * len(room_map)))
            print("".join(row))
            # print("".join(bottom_line * len(map)))

    @staticmethod
    def _shift_coordinates(current_coordinate, direction):
        if direction == "North":
            coordinates = (current_coordinate[0], current_coordinate[1] + 1)
        elif direction == "South":
            coordinates = (current_coordinate[0], current_coordinate[1] - 1)
        elif direction == "East":
            coordinates = (current_coordinate[0] + 1, current_coordinate[1])
        else:
            coordinates = (current_coordinate[0] - 1, current_coordinate[1])
        return coordinates

    def _stop(self):
        self.is_running = False
