from collections import OrderedDict
from unittest import TestCase
from game import Room, Game

class RoomTests(TestCase):
    def test_single_room_no_exits(self):
        room = Room("this is a test room")
        self.assertTrue(room.exits == {})

    def test_connect_two_rooms(self):
        rooms = [Room("test room 1"), Room("test room 2")]
        rooms[0].connect(rooms[1],"North")
        self.assertTrue(rooms[0].exits["North"] == rooms[1])

    def test_connect_all_directions(self):
        rooms = [Room('test'+str(d)) for d in range(1, 6)]
        for index, dir in enumerate(["North", "South", "East", "West"]):
            rooms[0].connect(rooms[index+1], dir)
        self.assertTrue(rooms[0].exits["North"] == rooms[1])
        self.assertTrue(rooms[0].exits["South"] == rooms[2])
        self.assertTrue(rooms[0].exits["East"] == rooms[3])
        self.assertTrue(rooms[0].exits["West"] == rooms[4])
        self.assertTrue(rooms[1].exits["South"] == rooms[0])
        self.assertTrue(rooms[2].exits["North"] == rooms[0])
        self.assertTrue(rooms[3].exits["West"] == rooms[0])
        self.assertTrue(rooms[4].exits["East"] == rooms[0])

    def test_connect_invalid_direction(self):
        rooms = [Room("test room 1"), Room("test room 2")]
        with self.assertRaises(ValueError):
            rooms[0].connect(rooms[1], "invalid")


# (Kind of gross) test strategy
def _test_strategy():
    # no variables exist
    direction = ["North", "South", "East", "West"][_test_strategy.dir_index]
    _test_strategy.dir_index = (_test_strategy.dir_index + 1) % 4
    return direction  # destroys dir_index
_test_strategy.dir_index = 0


class GameTests(TestCase):
    # TODO: single room no exits in game
    def setUp(self):
        _test_strategy.dir_index = 0

    def test_move(self):
        rooms = ["test room 1", "test room 2"]
        room_one = Room(rooms[0])
        room_two = Room(rooms[1])
        game = Game([room_one, room_two], _test_strategy)
        self.assertEquals(game.current_location,room_one)
        game.move("North")
        self.assertEquals(game.current_location,room_two)

    def test_move_bad_direction(self):
        rooms = ["test room 1", "test room 2"]
        room_one = Room(rooms[0])
        room_two = Room(rooms[1])
        game = Game([room_one, room_two], _test_strategy)
        self.assertEquals(game.current_location,room_one)
        with self.assertRaises(ValueError):
            game.move("invalid")

    def test_two_room_exits(self):
        rooms = ["test room 1", "test room 2"]
        room_one = Room(rooms[0])
        room_two = Room(rooms[1])
        game = Game([room_one, room_two], _test_strategy)
        self.assertEquals(game.current_location.exits["North"], room_two)
        self.assertEquals(room_two.exits["South"], game.current_location)

    def test_six_room_exits(self):
        room_descriptions = OrderedDict()
        room_descriptions['first'] = "the first room"
        room_descriptions['second'] = "the second room"
        room_descriptions['third'] = "the third room"
        room_descriptions['fourth'] = "the fourth room"
        room_descriptions['fifth'] = "the fifth room"
        room_descriptions['sixth'] = "the sixth room"
        rooms = [Room(r) for r in room_descriptions]
        game = Game(rooms, _test_strategy)
        game.move("North")
        self.assertEquals(game.current_location, rooms[1])
        game.move("East")
        self.assertEquals(game.current_location, rooms[2])
        game.move("North")
        self.assertEquals(game.current_location, rooms[3])
        game.move("East")
        self.assertEquals(game.current_location, rooms[4])
        game.move("North")
        self.assertEquals(game.current_location, rooms[5])

    def test_move_two_rooms_exits(self):
        rooms = ["test room 1", "test room 2"]
        room_one = Room(rooms[0])
        room_two = Room(rooms[1])
        game = Game([room_one, room_two], _test_strategy)
        game.move("North")
        self.assertEquals(game.current_location, room_two)

# TODO: Test print_map
# TODO: Test print_map and only show discovered rooms
# TODO: Test get_status
# TODO: Test parse_user_input