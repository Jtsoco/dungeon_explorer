from HUD.text import Text
class MenuData:
    # here we need a menu to hold elements like the hud does, probably an ordered list of menu items that can be moved up and down through, and selected
    # also means it needs to change current selection, but really that's just changing the index of the selected item in the list
    # question is, will select return something, or send a load event for what to load next, like an enum that says 'inventory' or 'settings' or 'start)game' and then app handles that
    def __init__(self, menu_type, title="Main Menu"):


        self.menu_options = []
        self.menu_components = []
        self.current_selection_index = 0
        self.title = Text(content=title, position=(24, 8))
        self.menu_type = menu_type


    def add_option(self, menu_option):
        self.menu_options.append(menu_option)

    def index_up(self):
        if not self.current_selection().index_up() and (self.current_selection_index > 0):
            # returning false means the menu component has reached the end of its items
            self.current_selection_index -= 1

    def index_down(self):
        component_index_changed = self.current_selection().index_down()
        # if false, it can't move down anymore, and need to move to next component if possible

        if not component_index_changed and (self.current_selection_index < len(self.menu_components) - 1):
            self.current_selection_index += 1


    def index_left(self):
        self.current_selection().index_left()

    def index_right(self):
        self.current_selection().index_right()

    def current_selection(self):
        return self.menu_components[self.current_selection_index]

    def get_current_selection(self):
        return self.menu_components[self.current_selection_index].get_current_selection()

    def add_component(self, menu_component):
        self.menu_components.append(menu_component)

    def items_to_draw(self):
        items = []
        for component in self.menu_components:
            items.extend(component.items_to_draw())
        return items

    def get_characters_to_draw(self):
        characters = []
        for component in self.menu_components:
            characters.extend(component.characters_to_draw())
        return characters

    def get_horizontal_components(self):
        horizontal_components = []
        for component in self.menu_components:
            if len(component.horizontal_options) > 0:
                horizontal_components.append(component)
        return horizontal_components
