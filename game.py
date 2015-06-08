from random import sample
from models import Room, Player

DIRECTIONS = ['North', 'South', 'East', 'West', 'N', 'S', 'E', 'W']


def _choose_random_direction():
    # Requires: N/A
    # Ensures: returns one of the strings at random - "North", "South", "East", or "West"
    return sample(["North", "South", "East", "West"], 1)[0]

class Game:
    rooms = None
    is_running = False
    coordinate_map = None
    current_coordinate = (0, 0)
    events = None

    def __init__(self, rooms, direction_strategy=_choose_random_direction):  # TODO: Test this
        # Requires: an iterable object containing Room objects, a strategy for assigning rooms
        # Ensures:
        # assignment of instance variables(events, rooms,coordinate_map,is_running)
        # creation of coordinate_ map by calling make_map method
        # instantiation of Player and sets its location instance variable to coordinate 0,0
        # assignment to receiver list for player events (per Observer pattern)
        self.events = []
        self.rooms = rooms
        for room in rooms:
            room.add_receiver(self)
        self.coordinate_map = {(0, 0): rooms[0]}  # prevents self-connection of first room
        self._make_map(direction_strategy)
        self.player = Player(rooms[0])
        self.player.add_receiver(self)
        self.is_running = True

    def receive(self, event):
        # Requires: an instance of an Event object
        # Ensures: events instance variable iterable object contains the passed Event object
        self.events.append(event)

    def get_status(self):  # TODO: test this
        # Requires: N/A
        # Ensures: returns a blank-line separated string of event messages from
        #          events instance variable.
        status = ""
        for event in self.events:
            status += event.message + "\n"
        self.events = []
        return status

    def respond_to_user_input(self, user_input):  # TODO: test this
        # Requires: a string containing desired action
        # Ensures:
        # proper selection and calls move, look, map or exit action
        # OR
        # prints feedback to user that desired action is unavailable
        # TODO: get rid of print call here and return instead.
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
        elif user_input in ["Quit", "Q"]:
            self.is_running = False
        else:
            print("sorry, there is no such action")

    def _make_map(self, direction_strategy):
        # Requires: a direction strategy to use in assigning room directions and exits
        # Ensures:
        # assignment of coordinates to corresponding room objects in coordinates_map:
        # rooms are assigned per logical directions.
        # connection of rooms via room's exits instance variable
        # rooms are connected logically
        # i.e. if a user goes N, W, S, the first room & final rooms are connected by E/W

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

    def print_map(self):  # TODO: make this return instead?
        # Requires: make_map must have already been called.
        # Ensures:
        # creates a printed map to the command line.
        # resulting map shows only those rooms which have been discovered by the player
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

    @staticmethod
    def _shift_coordinates(current_coordinate, direction):
        # Requires:
        # current_coordinate instance variable be instantiated
        # string-ified direction be passed
        # Ensures:
        # returns a tuple of coordinates
        # returned coordinates are logically created by a shift in the given direction
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
        # Requires: N/A
        # Ensures: re-assignment of is_running instance variable to False
        self.is_running = False
