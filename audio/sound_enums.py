from enum import Enum

class SoundEnum(Enum):

# these enums are the values put into pyxel sound slots
    ATTACK = 0
    JUMP = 1
    LAND = 2
    DAMAGE = 3
    DEATH = 4
    BREAK = 5
    BLOCK = 6
    UNBLOCK = 7
    # EXPLOSION = auto()

class MusicEnum(Enum):
    BACKGROUND_MUSIC = 0
    BOSS_MUSIC = 1
