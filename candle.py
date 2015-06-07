from collections import OrderedDict
from game import Game
from models import Room

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
rooms['Sun room'] = "This room would be beautiful and full of sun during the day, but right now it is " \
                    "creepy by moonlight."
rooms['Smoking room'] = "This room smells disgustingly of old cigars. You imagine it was a smoking room."
rooms['Hallway'] = "This is a long hallway"

if __name__ == "__main__":
    game_rooms = [Room(name, desc) for name, desc in rooms.items()]
    # for room in game_rooms:
    #     room.is_discovered = True
    game = Game(game_rooms)
    # game.print_map()
    #
    #
    print(TITLE)
    print()
    print(INTRO)
    print()

    while game.is_running:
        print(game.current_status)
        game.respond_to_user_input(input(PROMPT))
        print("\n \n")
