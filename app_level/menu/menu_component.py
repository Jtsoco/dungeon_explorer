# this holds menu related options, and manages index up and down, and upon selection returns active items selection
# this is the base class to be inherited from, for things like inventory, and regular selections
class MenuComponent():
    def __init__(self, pos, x_offset, y_offset):
        self.options = []
        # for multiple options, a 2d array could be used later
        self.position = pos
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.y_index = 0
        self.x_index = 0
        # secondary is used for options within options

    def setup_options(self, options):
        x = self.position[0]
        y = self.position[1]



        return (x, y)

    def up_index(self):
        # adjust own index up or down
        if self.y_index > 0:
            self.y_index -= 1
            return True
        return False

    def down_index(self):
        if self.y_index < len(self.options) - 1:
            self.y_index += 1
            return True
        return False

    def right_index(self):

        return False

    def left_index(self):
        return False

class TwoDMenuComponent(MenuComponent):
    def __init__(self, pos, x_offset, y_offset):
        super().__init__(pos, x_offset, y_offset)
        # 2d menu will have both x and y indexes
        self.x_index = 0
        self.y_index = 0
        self.options = [[]]  # initialize as 2d list

    def up_index(self):
        if self.y_index > 0:
            self.y_index -= 1
            return True
        return False

    def down_index(self):
        if self.y_index < len(self.options) - 1:
            self.y_index += 1
            return True
        return False

    def right_index(self):
        if self.x_index < len(self.options[self.y_index]) - 1:
            self.x_index += 1
            return True
        return False

    def left_index(self):
        if self.x_index > 0:
            self.x_index -= 1
            return True
        return False
