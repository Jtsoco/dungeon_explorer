from HUD.text import Text
from entity.entity_setup import spawn_player
class MenuOption():
    # the default text option of a menu,
    # has text, position, and action to perform on select
    def __init__(self, text, position=(0,0), action=None):
        self.text = Text(content=text, position=position)
        self.action = action  #enum for action to perform on select


class CharacterMenuOption(MenuOption):
    def __init__(self, character, position=(0,0), action=None):
        super().__init__(text=character.name, position=position, action=action)
        self.character = spawn_player(p_type=character)

class ItemMenuOption(MenuOption):
    def __init__(self, item, position=(0,0), action=None):
        super().__init__(text="", position=position, action=action)
        self.item = item
