class Room:
    name = ""  # name must be fewer than 20 chars long
    description = ""
    exits = None
    is_discovered = False
    name_string = None

    def __init__(self, name="", description=""):
        self.name = name
        # TODO: validate name length < 20
        self.description = description
        self.exits = {}
        self._make_pretty_box()

    # TODO: test init


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

    def _make_pretty_box(self):
        box_width = 20  # this is/will be a constraint set on the name of the room class
        offset = box_width - len(self.name)
        side_line = "|"

        # box line creation logic
        if offset % 2 == 0:
            first_offset = int(offset / 2)
            second_offset = first_offset
        else:
            first_offset = int(offset / 2)
            second_offset = first_offset + 1

        box_name_line = side_line + (" " * first_offset) + self.name + (" " * second_offset) + ""
        self.name_string = box_name_line

    def describe(self):
        strings = []
        if not self.is_discovered:
            strings.append(self.description)
        else:
            strings.append('You are back in the {}.'.format(self.name))
        strings += ['There is an exit to the {}.'.format(k) for k in self.exits.keys()]
        return '\n'.join(strings)
