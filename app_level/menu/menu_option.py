from HUD.text import Text
class MenuOption():
    # the default text option of a menu,
    # has text, position, and action to perform on select
    def __init__(self, text, position=(0,0), action=None):
        self.text = Text(content=text, position=position)
        self.action = action  #enum for action to perform on select
