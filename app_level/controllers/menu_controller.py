from app_level.controllers.app_controller import AppController
import pyxel
from app_level.app_enums import MenuCommandTypes
from app_level.app_commands_events import MenuCommand

class MenuController(AppController):
    def __init__(self, bus):
        super().__init__(bus)
        # setup menu specific things here

    def handle_inputs(self):
        recents = set()
        # handle menu specific inputs here

        # when up arrow pressed, send a go up command
        # when down arrow pressed, send a go down command
        # when enter pressed, send a select command
        # when backspace pressed, send a go back command

        # for later, when right or left pressed, send respective commands
        if pyxel.btn(pyxel.KEY_RETURN):
            recents.add(pyxel.KEY_RETURN)
        if pyxel.btn(pyxel.KEY_UP):
            recents.add(pyxel.KEY_UP)
        if pyxel.btn(pyxel.KEY_DOWN):
            recents.add(pyxel.KEY_DOWN)
        if pyxel.btn(pyxel.KEY_LEFT):
            recents.add(pyxel.KEY_LEFT)
        if pyxel.btn(pyxel.KEY_RIGHT):
            recents.add(pyxel.KEY_RIGHT)
        if pyxel.btn(pyxel.KEY_TAB):
            recents.add(pyxel.KEY_TAB)

        return recents

    def send_command(self, command_type):
        command = MenuCommand(action=command_type)
        self.bus.send_command(command)

    def process_keys(self, new_recents):
        commands = set()
        for key in new_recents:
            match key:
                case pyxel.KEY_RETURN:
                    commands.add(MenuCommandTypes.SELECT)
                case pyxel.KEY_UP:
                    commands.add(MenuCommandTypes.UP)
                case pyxel.KEY_DOWN:
                    commands.add(MenuCommandTypes.DOWN)
                case pyxel.KEY_LEFT:
                    commands.add(MenuCommandTypes.LEFT)
                case pyxel.KEY_RIGHT:
                    commands.add(MenuCommandTypes.RIGHT)
                case pyxel.KEY_TAB:
                    commands.add(MenuCommandTypes.QUIT)

        return commands
