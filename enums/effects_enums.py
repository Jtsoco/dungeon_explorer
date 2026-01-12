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
