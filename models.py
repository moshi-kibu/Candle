class Event:
    message = ""

    def __init__(self, message):
        # Requires: string to be passed in
        # Ensures: the instance variable message is assigned to the string passed in.
        self.message = message


class Sender:
    receivers = None

    def __init__(self):
        # Requires: N/A
        # Ensures: the instance variable receivers is initialized as an empty set.
        self.receivers = set()

    def send(self, event):  # TODO: Test this
        # Requires: an event object to be passed in
        # Ensures: each subscribed receiver is passed the event object
        for receiver in self.receivers:
            receiver.receive(event)

    def add_receiver(self, receiver):  # TODO: Test this
        # Requires: a receiver object to be passed in
        # Ensures:
        # the passed in receiver is signed up for updates from this object.
        # the receiver is added to the instance variable iterable object receiver.
        # receivers can only subscribe a single time for updates from a given sender
        self.receivers.add(receiver)


class Room(Sender):
    name = ""  # name must be fewer than 20 chars long
    description = ""
    exits = None
    is_discovered = False
    name_string = None

    def __init__(self, name="", description=""):  # TODO: test init
        # Requires: N/A
        # Ensures:
        # inherits methods from Sender class
        # sets name and description instance variables if optional values are passed
        # sets exits as an empty dictionary for later processing by Game object
        # calls _make_room_map_title_line to set instance variable of name_string
        super().__init__()
        self.name = name
        # TODO: validate name length < 20
        self.description = description
        self.exits = {}
        self._make_room_map_title_line()

    def __str__(self):
        # Requires: N/A
        # Ensures: when Room object is printed, the instance variable description
        #          is passed to the print method.
        return self.description

    def visit(self):  # TODO: test this
        # Requires: N/A
        # Ensures:
        # sends an update to all subscribed receivers
        # sends an Event object calling the describe method as the message
        # resets the instance variable is_discovered to True
        self.send(Event(self.describe()))
        self.is_discovered = True

    def describe(self):  # TODO: test this
        strings = []
        if not self.is_discovered:
            strings.append(self.description)
        else:
            strings.append('You are back in the {}.'.format(self.name))
        strings += ['There is an exit to the {}.'.format(k) for k in self.exits.keys()]
        return '\n'.join(strings)

    def connect(self, room, direction):  # TODO test this
        # Requires: a Room object and a string representing the direction
        # Ensures:
        # self is connected to given room in given direction
        # given room is connected to self in opposite direction
        # rooms are connected via exits instance variable on each Room object
        # if invalid direction is passed, ValueError is raised
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

    def _make_room_map_title_line(self):
        # Requires: N/A
        # Ensures:
        # sets instance variable name_string to string created by this method
        # string represents the middle line of the room's representation on the map.
        box_width = 20  # this is/will be a constraint set on the name of the room class
        offset = box_width - len(self.name)
        side_line = "|"

        # line creation logic
        if offset % 2 == 0:
            first_offset = int(offset / 2)
            second_offset = first_offset
        else:
            first_offset = int(offset / 2)
            second_offset = first_offset + 1

        box_name_line = side_line + (" " * first_offset) + self.name + (" " * second_offset) + ""
        self.name_string = box_name_line


class Player(Sender):
    location = None

    def __init__(self, location):
        # Requires: Room object to be passed in.
        # Ensures:
        # Player inherits methods from Sender class
        # sets the instance variable location to passed in Room object
        # calls the visit method on the passed in Room
        super().__init__()
        self.location = location
        self.location.visit()
        self.options()

    def move(self, direction):  # TODO: fix breaking tests on this

        try:
            self.location = self.location.exits[direction]
            self.send(Event("You move to the " + direction + "."))
            self.location.visit()
        except KeyError:  # no exit this way
            self.send(Event("There's no exit that way, dorkface."))

    def look(self):  # TODO: test this
        self.location.is_discovered = False
        self.location.visit()

    def options(self):  # TODO: test this
        message = "You can move by entering the name of a direction, or its first letter. \n" \
                  "You can view the map by typing map or m. \n" \
                  "You can look by typing look or l. \n" \
                  "You can see these options again by typing options or o."
        self.send(Event(message))
