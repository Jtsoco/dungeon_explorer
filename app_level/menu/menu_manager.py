from base_manager import BaseManager
from app_level.menu.menu_data import MenuData
from app_level.menu.menu_renderer import MenuRenderer
from app_level.app_commands_events import MenuCommand, StateChangeEvent
from app_level.app_enums import MenuCommandTypes


class MenuManager(BaseManager):
    def __init__(self, context=None, bus=None):
        super().__init__(context)
        # this will primarily handle menu related events and commands
        self.menu_title = "Main Menu"
        self.renderer = MenuRenderer()
        self.bus = bus
        self.menu_data = None
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


    def handle_event(self, event):
        # handle menu related events
        pass

    def draw(self):
        if self.menu_data:
            self.renderer.render(self.menu_data)

    def handle_menu_command(self, command):
        match command.action:
            case MenuCommandTypes.UP:
                self.menu_data.index_up()
            case MenuCommandTypes.DOWN:
                self.menu_data.index_down()
            case MenuCommandTypes.SELECT:
                self.execute_current_selection()

    def execute_current_selection(self):
        current_option = self.menu_data.menu_options[self.menu_data.current_selection_index]
        action = current_option.action
        # Here we would handle the action, e.g., changing menus or executing commands
        # For now, we will just print the action
        self.bus.send_event(StateChangeEvent(new_state=action))
