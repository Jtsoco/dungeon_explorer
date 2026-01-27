from app_level.controllers.app_controller import AppController

import pyxel

from app_level.app_enums import MenuCommandTypes, MenuState
from app_level.app_commands_events import MenuCommand, StateChangeEvent

class GameController(AppController):
    def __init__(self, bus):
        super().__init__(bus)
        # setup game specific things here

    def update(self):
        new_recents = set()
        new_recents.update(self.handle_inputs())
        new_keys = new_recents - self.recent_keys
        events_to_send = self.process_keys(new_keys)
        # the game controller only sends events, and it actually only sends one event, the pause menu event, but that is acted upon instantly by app, unlike commands which go through menu managers and only update during their loop, so recent keyes needs to be updated here otherwise it will be skipped before the next controller is setup
        # honestly should probably have it go through menu manager, but fine for now
        self.recent_keys = new_recents
        for event in events_to_send:
            self.send_event(event)

    def handle_inputs(self):
        recents = set()
        # handle game specific inputs here
        if pyxel.btn(pyxel.KEY_TAB):
            recents.add(pyxel.KEY_TAB)
        return recents

    def send_event(self, command):
        state_event = StateChangeEvent(new_state=command)
        self.bus.send_event(state_event)

    def process_keys(self, new_recents):
        # this is using the process of app, so instead of commands
        states = set()
        for key in new_recents:
            match key:
                case pyxel.KEY_TAB:
                    states.add(MenuState.PAUSE_MENU)

        return states
