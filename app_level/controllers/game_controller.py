from app_level.controllers.app_controller import AppController

import pyxel

from app_level.app_enums import MenuCommandTypes, MenuState
from app_level.app_commands_events import MenuCommand, StateChangeEvent

class GameController(AppController):
    def __init__(self, bus):
        super().__init__(bus)
        # setup game specific things here

    def handle_inputs(self):
        recents = set()
        # handle game specific inputs here
        if pyxel.btn(pyxel.KEY_TAB):
            recents.add(MenuState.PAUSE_MENU)
        return recents

    def send_command(self, command):
        command = StateChangeEvent(new_state=command)
        self.bus.send_event(command)
