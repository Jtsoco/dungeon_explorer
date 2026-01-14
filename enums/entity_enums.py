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
    BLOCK = auto()
    STOP_BLOCK = auto()

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
    PLAYER = (3, 10)
    SKULL = (3, 15)
    KNIGHT = (3, 16)
    WINGED_KNIGHT = (3, 23)
    # this spawn won't be used, just for the player costume
    PLAYER_RONIN = (3, 30)


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
    GLAIVE = auto()
    KATANA = auto()

class BoundaryType(Enum):
    X = (3, 8)
    Y = (3, 9)

class SimpleAIState(Enum):
    PATROL = auto()
    CHASE = auto()
    ATTACK = auto()
    FLEE = auto()
    JUMP_ATTACK = auto()

class PowerUpStates(Enum):
    DOUBLE_JUMP = auto()

class SHIELD_ACTION_STATE(Enum):
    IDLE = auto()
    TO_BLOCK = auto()
    BLOCK = auto()
    DEFLECT = auto()
    TO_REST = auto()
    BROKEN = auto()

class SHIELD_CATEGORY(Enum):
    WOODEN_SHIELD = auto()
    IRON_SHIELD = auto()
    MAGIC_SHIELD = auto()
    BLADE = auto()
    DAGGER = auto()
