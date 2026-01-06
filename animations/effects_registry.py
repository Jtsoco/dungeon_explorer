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
        AnimationFrame((0,28)),
        AnimationFrame((1,28)),
        AnimationFrame((0,29)),
        AnimationFrame((1,29)),
        AnimationFrame((0,30)),
        AnimationFrame((1,30)),
    ],
}
set_lengths_according_to_fps(PARTICLE_REGISTRY[ParticleEffectType.JUMP_DUST], seconds=0.3)
set_offset(PARTICLE_REGISTRY[ParticleEffectType.JUMP_DUST], offset=(0,2))
set_lengths_according_to_fps(PARTICLE_REGISTRY[ParticleEffectType.LAND_DUST], seconds=0.3)

EFFECTS_REGISTRY = {
    EffectType.PARTICLE: PARTICLE_REGISTRY,
}
