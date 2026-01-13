from HUD.text import Text
class MenuData:
    # here we need a menu to hold elements like the hud does, probably an ordered list of menu items that can be moved up and down through, and selected
    # also means it needs to change current selection, but really that's just changing the index of the selected item in the list
    # question is, will select return something, or send a load event for what to load next, like an enum that says 'inventory' or 'settings' or 'start)game' and then app handles that
    def __init__(self, menu_type, title="Main Menu"):


        self.menu_options = []
        self.current_selection_index = 0
        self.title = Text(content=title, position=(24, 8))
        self.menu_type = menu_type


    def add_option(self, menu_option):
        self.menu_options.append(menu_option)

    def index_up(self):
        if self.current_selection_index > 0:
            self.current_selection_index -= 1

    def index_down(self):
        if self.current_selection_index < len(self.menu_options) - 1:
            self.current_selection_index += 1
