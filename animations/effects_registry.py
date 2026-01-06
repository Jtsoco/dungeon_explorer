from enums.effects_enums import EffectType, ParticleEffectType
from animations.animation_frame import AnimationFrame
from animations.frame_module import set_lengths_according_to_fps, set_offset
PARTICLE_REGISTRY = {
    ParticleEffectType.JUMP_DUST: [
        AnimationFrame((2,23)),
        AnimationFrame((2,24)),
        AnimationFrame((2,25)),
        AnimationFrame((2,26)),
    ],
    ParticleEffectType.LAND_DUST: [
        AnimationFrame((3,11)),
        AnimationFrame((4,11)),
        AnimationFrame((3,12)),
        AnimationFrame((4,12)),
        AnimationFrame((3,13)),
        AnimationFrame((4,13)),
    ],
}
set_lengths_according_to_fps(PARTICLE_REGISTRY[ParticleEffectType.JUMP_DUST], seconds=0.3)
set_offset(PARTICLE_REGISTRY[ParticleEffectType.JUMP_DUST], offset=(0,2))

EFFECTS_REGISTRY = {
    EffectType.PARTICLE: PARTICLE_REGISTRY,
}
