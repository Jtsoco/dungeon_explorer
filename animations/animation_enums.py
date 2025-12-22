from enum import Enum

class PlayerAnimationEnums(Enum):
    # Assuming tile map positions (u, v) for 16x16 sprites; adjust based on your .pyxres
    PLAYER_IDLE_1 = (0, 6)
    PLAYER_WALK_1 = (0, 7)
    PLAYER_WALK_2 = (1, 7)
    PLAYER_JUMP = (0, 9)
    PLAYER_FALL = (0, 10)
    # Add more as needed

class SkullAnimationEnums(Enum):
    SKULL_IDLE_1 = (0, 15)
    SKULL_WALK_1 = (0, 15)
    SKULL_WALK_2 = (1, 15)
    # Add more as needed

class GenericDeathAnimationEnums(Enum):
    DEATH_1 = (0, 20)
    DEATH_2 = (1, 20)
    DEATH_3 = (0, 21)
    DEATH_4 = (1, 21)
    DEATH_5 = (0, 22)
    DEATH_6 = (1, 22)
    # Add more as needed
