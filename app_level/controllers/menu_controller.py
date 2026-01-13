from app_level.controllers.app_controller import AppController
import pyxel
from app_level.app_enums import MenuCommandTypes
from app_level.app_commands_events import MenuCommand

class MenuController(AppController):
    def __init__(self, context):
        super().__init__(context)
        # setup menu specific things here

    def handle_inputs(self):
        recents = set()
        # handle menu specific inputs here

        # when up arrow pressed, send a go up command
        # when down arrow pressed, send a go down command
        # when enter pressed, send a select command
        # when backspace pressed, send a go back command

        # for later, when right or left pressed, send respective commands
        if pyxel.btn(pyxel.KEY_KP_ENTER):
            recents.add(MenuCommand(action=MenuCommandTypes.SELECT))
        if pyxel.btn(pyxel.KEY_UP):
            recents.add(MenuCommand(action=MenuCommandTypes.UP))
        if pyxel.btn(pyxel.KEY_DOWN):
            recents.add(MenuCommand(action=MenuCommandTypes.DOWN))

        return recents
