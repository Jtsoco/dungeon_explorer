from enum import Enum, auto

class MenuCommandTypes(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    SELECT = auto()
    QUIT = auto()
    TO_MAIN_MENU = auto()

class MenuState(Enum):
    MAIN_MENU = auto()
    OPTIONS = auto()
    PAUSE_MENU = auto()
    INVENTORY = auto()
    GAME_OVER = auto()
    QUIT = auto()
    CHARACTER_SELECT = auto()
    HORIZONTAL_SELECT = auto()
    WEAPON_SELECT = auto()
    SHIELD_SELECT = auto()

    # the game enum references when the actual game is being played
    GAME = auto()
