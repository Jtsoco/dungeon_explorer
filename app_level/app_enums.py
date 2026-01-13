from enum import Enum, auto

class MenuCommandTypes(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    SELECT = auto()
    BACK = auto()
    QUIT = auto()

class MenuState(Enum):
    MAIN_MENU = auto()
    OPTIONS = auto()
    PAUSE_MENU = auto()
    INVENTORY = auto()
    GAME_OVER = auto()

    # the game enum references when the actual game is being played
    GAME = auto()
