from base_manager import BaseManager
from app_level.menu.menu_data import MenuData
from app_level.menu.menu_renderer import MenuRenderer
from app_level.app_commands_events import MenuCommand
from app_level.app_enums import MenuCommandTypes


class MenuManager(BaseManager):
    def __init__(self, context=None):
        super().__init__(context)
        # this will primarily handle menu related events and commands
        self.menu_title = "Main Menu"
        self.current_menu = None
        self.renderer = MenuRenderer()

    def set_menu(self, menu):
        self.current_menu = menu

    def handle_command(self, command):
        # handle menu related commands
        if isinstance(command, MenuCommand):
            self.handle_menu_command(command)


    def handle_event(self, event):
        # handle menu related events
        pass

    def draw(self):
        if self.current_menu:
            self.renderer.render(self.current_menu)

    def handle_menu_command(self, command):
        match command.action:
            case MenuCommandTypes.UP:
                self.menu_data.index_up()
            case MenuCommandTypes.DOWN:
                self.menu_data.index_down()
            case MenuCommandTypes.SELECT:
                self.execute_current_selection()

    def execute_current_selection(self):
        current_option = self.current_menu.menu_options[self.current_menu.current_selection_index]
        action = current_option.action
        # Here we would handle the action, e.g., changing menus or executing commands
        # For now, we will just print the action
        print(f"Executing action: {action}")
