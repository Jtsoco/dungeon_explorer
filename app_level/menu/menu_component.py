# this holds menu related options, and manages index up and down, and upon selection returns active items selection
# this is the base class to be inherited from, for things like inventory, and regular selections
from app_level.menu.menu_option import MenuOption
from HUD.text import Text
from enums.entity_enums import EntityType

class MenuComponent():
    def __init__(self, pos, x_offset, y_offset, title=None):
        self.options = []
        # for multiple options, a 2d array could be used later
        self.position = pos
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.y_index = 0
        self.x_index = 0
        if title:
            self.title = Text(content=title, position=(pos[0], pos[1] - 10))
        else:
            self.title = None
        # secondary is used for options within options

    def get_current_selection(self):
        return self.options[self.y_index]

    def setup_options(self, options):
        x = self.position[0]
        y = self.position[1]
        for option in options:
            option.text.position = (x, y)
            self.options.append(option)
            y += self.y_offset

    def add_option(self, option):
        option.text.position = (self.position[0], self.position[1] + len(self.options) * self.y_offset)
        self.options.append(option)

    def get_bottom_y(self):
        return self.y_offset * len(self.options) + self.position[1]


    def setup_options(self, options):
        x = self.position[0]
        y = self.position[1]
        return (x, y)

    def index_up(self):
        # adjust own index up or down
        if self.y_index > 0:
            self.y_index -= 1
            return True
        return False

    def index_down(self):
        if self.y_index < len(self.options) - 1:
            self.y_index += 1
            return True
        return False

    def index_right(self):

        return False

    def index_left(self):
        return False

    def items_to_draw(self):
        items = []
        if self.title:
            items.append(self.title)
        for option in self.options:
            items.append(option.text)
        return items

class TwoDMenuComponent(MenuComponent):
    def __init__(self, pos, x_offset, y_offset):
        super().__init__(pos, x_offset, y_offset)
        # 2d menu will have both x and y indexes
        self.x_index = 0
        self.y_index = 0
        self.options = [[]]  # initialize as 2d list

    def index_up(self):
        if self.y_index > 0:
            self.y_index -= 1
            return True
        return False

    def index_down(self):
        if self.y_index < len(self.options) - 1:
            self.y_index += 1
            return True
        return False

    def index_right(self):
        if self.x_index < len(self.options[self.y_index]) - 1:
            self.x_index += 1
            return True
        return False

    def index_left(self):
        if self.x_index > 0:
            self.x_index -= 1
            return True
        return False

    def get_current_selection(self):
        return self.options[self.y_index][self.x_index]

class HorizontalMenuComponent(MenuComponent):
    def __init__(self, pos, x_offset, y_offset, title=None):
        super().__init__(pos, x_offset, y_offset, title)

    def index_up(self):
        return False

    def index_down(self):
        return False

    def index_right(self):
        if self.x_index < len(self.options) - 1:
            self.x_index += 1
            return True
        return False

    def index_left(self):
        if self.x_index > 0:
            self.x_index -= 1
            return True
        return False

    def get_current_selection(self):
        return self.options[self.x_index]

    def items_to_draw(self):
        items = []
        if self.title:
            items.append(self.title)
        for option in self.options:
            items.append(option.text)
        return items

class CharacterSelectMenuComponent(HorizontalMenuComponent):
    def __init__(self, pos, x_offset, y_offset, title="Select Character"):
        super().__init__(pos, x_offset, y_offset, title)


    def character_to_draw(self):
        current_option = self.get_current_selection()
        return current_option.character
