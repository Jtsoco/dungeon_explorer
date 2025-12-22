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

class AttackType(Enum):
    MELEE = auto()
    RANGED = auto()


class WeaponActionState(Enum):
    SHEATHED = auto()
    DRAWN = auto()
    DASHATTACK = auto()
    AIRATTACK = auto()
    DEFAULT = auto()

class EntityType(Enum):
    # not including player for now
    PLAYER = (3, 10)
    SKULL = (3, 15)
    KNIGHT = (3, 16)

class EntityCategory(Enum):
    FLYING = auto()
    GROUND = auto()

class CollisionEnums(Enum):
    ENTITY = auto()
    PROJECTILE = auto()
    ENVIRONMENT = auto()

class CollisionEntityTarget(Enum):
    PLAYER = auto()
    ENEMY = auto()
    ALL = auto()

class WeaponCategory(Enum):
    SHORTSWORD = auto()
    BOW = auto()
    STAFF = auto()
    AXE = auto()
