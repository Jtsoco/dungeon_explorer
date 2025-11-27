from enum import Enum, auto

class MovementState(Enum):
    IDLE = auto()
    WALKING = auto()
    JUMPING = auto()
    FALLING = auto()

class DirectionState(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    HALT = auto()

class ActionState(Enum):
    NONE = auto()
    ATTACKING = auto()
    DEFENDING = auto()

class InputEnums(Enum):
    NONE = auto()
    MOVE = auto()
    JUMP = auto()
    ATTACK = auto()
    STOP_MOVE = auto()
