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
from app_level.menu.menu_manager import MenuManager
from system.system_buses import SystemBus
from app_level.app_commands_events import StateChangeEvent
from app_level.controllers.menu_controller import MenuController
from app_level.app_enums import MenuState
from app_level.menu.menu_setup import setup_main_menu, setup_pause_menu
from app_level.controllers.menu_controller import MenuController
from app_level.controllers.game_controller import GameController

import pyxel
TRANSPARENT_COLOR = 2
from game import Game
from datetime import datetime

class App():
    def __init__(self):
        pyxel.init(128, 128, title="Dungeon Explorer")
        pyxel.load("dungeon_explorer_assets.pyxres")
        # Hide the spawn and border transition tiles
        pyxel.images[0].rect(24, 64, 16, 72, TRANSPARENT_COLOR)

        # need bus for communication between systems
        # need game class to handle game loop
        # need menu class to handle menus and select games
        self.game = None
        # for an actual game, the menu would select the game (dungeon) to play
        self.running = False

        # for new app, menu system:
        # need bus for communication
        # app level controller to always be updated
        # state change event to be handled here to switch between menu and game
        # a stack of menu type enums or states to keep track of current menu
        # leaning towards enums, because game menus access data through context, so no need to keep full state objects for different menus
        # just reload menu each time based on enum
        # and if last selection is desired, just save it with last selection too, for the stack
        self.top_bus = SystemBus(False)
        self.menu_manager = MenuManager(bus=self.top_bus)
        self.top_bus.register_event_listener(StateChangeEvent, self)

        self.controller = MenuController(self.top_bus)

        self.current_update = None
        self.current_draw = None
        main_menu = setup_main_menu()
        self.menu_manager.set_menu(main_menu)
        self.setup_menu_mode()
        self.menu_stack = []

    def state_change_event(self, new_state):

        match new_state:
            case MenuState.MAIN_MENU:
                main_menu = setup_main_menu()
                if len(self.menu_stack) > 1:
                    # make sure a return to main menu from another menu resets to main menu
                    self.menu_stack = [MenuState.MAIN_MENU]
                else:
                    self.menu_stack.append(MenuState.MAIN_MENU)
                self.menu_manager.set_menu(main_menu)

                self.setup_menu_mode()
            case MenuState.PAUSE_MENU:
                self.menu_stack.append(MenuState.PAUSE_MENU)
                pause_menu = setup_pause_menu()
                self.menu_manager.set_menu(pause_menu)
                self.setup_menu_mode()
            case MenuState.GAME:
                self.setup_game_mode()
            case MenuState.QUIT:
                self.quit()

    def quit(self):
        if self.menu_stack:
            self.menu_stack.pop()
            if self.menu_stack:
                self.state_change_event(self.menu_stack[-1])
            else:
                self.state_change_event(MenuState.MAIN_MENU)
                pyxel.quit()
        else:
            pyxel.quit()

    def setup_menu_mode(self):
        self.setup_menu_controller()
        self.current_update = self.menu_manager.update
        self.current_draw = self.menu_manager.draw

    def setup_game_mode(self):
        self.menu_stack.append(MenuState.GAME)
        if not self.game:
            self.game = Game()
            self.menu_manager.game = self.game
        self.current_update = self.game.update
        self.current_draw = self.game.draw
        self.setup_game_controller()

    def notify_event(self, event):
        match event:
            case StateChangeEvent():
                self.state_change_event(event.new_state)

    def run(self):
        self.running = True

        pyxel.run(self.update, self.draw)


    def update(self):
        self.controller.update()
        self.current_update()

    def draw(self):
        # would actually draw the current active state, game for now
        pyxel.cls(0)
        self.current_draw()


    def setup_menu_controller(self):
        recents = self.controller.recent_keys.copy()
        # prevent losing recent commands when switching controllers
        self.controller = MenuController(self.top_bus)
        self.controller.recent_keys = recents

    def setup_game_controller(self):
        recents = self.controller.recent_keys.copy()
        self.controller = GameController(self.top_bus)
        self.controller.recent_keys = recents

app = App()
app.run()



# for handling border transitions, have it so when player is touching secret border zones, the camera will center x or y at that border zone (depending on the border zone marker)
