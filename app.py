# TODO map out everything on paper properly
# or in figma
# decide what interacts with what
# whether to use a bus system for events or not
# try to keep it simple, a fun challenge to make a dungeon explorer type game in pyxel
# think of:
# how to pass around startup_context
# keep track of what the active cell is
# how to keep camera synced with active cells
# probably just fine to use an event system to notify camera of cell changes
# and main game keeps track of what cell is active based on player position
# and will run multiple cells during a cell transition
import pyxel
TRANSPARENT_COLOR = 2
from game import Game
from datetime import datetime

class App():
    def __init__(self):
        pyxel.init(128, 128, title="Dungeon Explorer")
        pyxel.load("dungeon_explorer_assets.pyxres")
        # Hide the spawn and border transition tiles
        pyxel.images[0].rect(24, 64, 16, 240, TRANSPARENT_COLOR)

        # need bus for communication between systems
        # need game class to handle game loop
        # need menu class to handle menus and select games
        self.game = None
        # for an actual game, the menu would select the game (dungeon) to play
        self.running = False


    def run(self):
        self.running = True
        self.game = Game()
        print("Starting game loop...")
        pyxel.run(self.update, self.draw)


    def update(self):
        self.game.update()

    def draw(self):
        # would actually draw the current active state, game for now
        pyxel.cls(0)
        self.game.draw()


app = App()
app.run()



# for handling border transitions, have it so when player is touching secret border zones, the camera will center x or y at that border zone (depending on the border zone marker)
