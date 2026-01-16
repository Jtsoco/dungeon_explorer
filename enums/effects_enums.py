from enum import Enum, auto


class EffectType(Enum):
    PARTICLE = auto()
    LIGHT = auto()
    SOUND = auto()
    DEATH_ANIMATION = auto()


class ParticleEffectType(Enum):
    JUMP_DUST = auto()
    LAND_DUST = auto()
    EXPLOSION = auto()
    SPARKLES = auto()
    BREAK = auto()
    ENEMY_ATTACK_START = auto()

class DEATH_ANIMATION_TYPE(Enum):
    KNIGHT_FALL = auto()
    ENEMY_DISINTEGRATE = auto()
    PLAYER_HEART_SHATTER = auto()
    DEFAULT_DEATH = auto()
