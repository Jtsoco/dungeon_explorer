from enum import Enum, auto

class HUDComponentType(Enum):
    HEALTH = auto()
    SHIELD = auto()
    MANA = auto()
    STAMINA = auto()
    SCORE = auto()
    TIMER = auto()
    INVENTORY = auto()
    MINI_MAP = auto()
