from base_manager import BaseManager
from app_level.menu.menu_data import MenuData
from app_level.menu.menu_renderer import MenuRenderer
from app_level.app_commands_events import MenuCommand, StateChangeEvent, SetMainCharacterCommand
from app_level.app_enums import MenuCommandTypes, MenuState
from events_commands.commands import HUDCommand, HUDUpdateCommand
import pyxel


class MenuManager(BaseManager):
    def __init__(self, context=None, bus=None):
        super().__init__(context)
        # this will primarily handle menu related events and commands
        self.menu_title = "Main Menu"
        self.renderer = MenuRenderer()
        self.bus = bus
        self.menu_data = None
        self.game = None
        if bus:
            self.setup_menu_bus()

    def setup_menu_bus(self):
        # subscribe to menu related events and commands
        self.bus.register_command_listener(MenuCommand, self)

    def set_menu(self, menu):
        self.menu_data = menu

    def handle_command(self, command):
        # handle menu related commands
        if isinstance(command, MenuCommand):
            self.handle_menu_command(command)

    def get_characters_to_draw(self):
        characters = self.menu_data.get_characters_to_draw()
        return characters


    def handle_event(self, event):
        # handle menu related events
        pass

    def draw(self):

        self.renderer.render(self.menu_data, self.game)

    def handle_menu_command(self, command):
        # whenever a button is pressed, play basic sound
        pyxel.play(1, 1)
        match command.action:
            case MenuCommandTypes.UP:
                self.menu_data.index_up()
            case MenuCommandTypes.DOWN:
                self.menu_data.index_down()
            case MenuCommandTypes.LEFT:
                self.menu_data.index_left()
            case MenuCommandTypes.RIGHT:
                self.menu_data.index_right()
            case MenuCommandTypes.SELECT:
                self.execute_current_selection()

            case MenuCommandTypes.QUIT:
                self.bus.send_event(StateChangeEvent(new_state=MenuState.QUIT))
            case MenuCommandTypes.TO_MAIN_MENU:
                self.bus.send_event(StateChangeEvent(new_state=MenuState.MAIN_MENU))

    def execute_current_selection(self):
        current_option = self.menu_data.get_current_selection()
        action = current_option.action
        # Here we would handle the action, e.g., changing menus or executing commands
        # For now, we will just print the action
        match self.menu_data.menu_type:
            case MenuState.MAIN_MENU:
                if action == MenuState.GAME or action == MenuState.CHARACTER_SELECT:
                    self.set_character()
                    print('character set!')
                elif action == MenuState.HORIZONTAL_SELECT:
                    pass
                    # this isn't needed yet, character is set when game starts, but for things like sound and such, it would be good to get the horizontal select option, then send that out as its own event, so that will go here
            case MenuState.PAUSE_MENU:
                if action == MenuState.HORIZONTAL_SELECT:
                    self.pause_horizontal_select()
                    return
                # don't need to change state here


        self.bus.send_event(StateChangeEvent(new_state=action))

    def pause_horizontal_select(self):
        current_horizontal = self.menu_data.get_current_selection()
        # this gives back the option
        horizontals = self.menu_data.get_horizontal_components()
        for horizontal in horizontals:
            if horizontal.get_current_selection() == current_horizontal:
                option = horizontal.get_current_horizontal_selection()
                if option.action == MenuState.WEAPON_SELECT:
                    self.select_weapon(option)
                elif option.action == MenuState.SHIELD_SELECT:
                    self.select_shield(option)


    def select_weapon(self, option):
        weapon = option.item
        player = self.context.data_context.player_data
        player.weapon = weapon
        self.game.context.bus.send_command(HUDUpdateCommand())

    def select_shield(self, option):
        shield = option.item
        player = self.context.data_context.player_data
        player.shield = shield
        self.game.context.bus.send_command(HUDUpdateCommand())



    def set_character(self):
        characters = self.get_characters_to_draw()
            # this will return entity data, and when it's main menu their should only be one in the menu, the player selection
        if characters:
            player_entity = characters[0]
            self.bus.send_command(SetMainCharacterCommand(entity_data=player_entity))
