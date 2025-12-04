from enum import Enum

class PlayerAnimationEnums(Enum):
    # Assuming tile map positions (u, v) for 16x16 sprites; adjust based on your .pyxres
    PLAYER_IDLE_1 = (0, 6)
    PLAYER_WALK_1 = (0, 7)
    PLAYER_WALK_2 = (1, 7)
    PLAYER_JUMP = (0, 9)
    PLAYER_FALL = (0, 10)
    # Add more as needed
