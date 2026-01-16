from enums.effects_enums import EffectType, ParticleEffectType, DEATH_ANIMATION_TYPE
from animations.animation_frame import AnimationFrame
from animations.frame_module import set_lengths_according_to_fps, set_offset
from animations.animation_enums import GenericDeathAnimationEnums as GDAE

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

    ParticleEffectType.BREAK: [
        AnimationFrame((5,10)),
        AnimationFrame((6,10)),

    ],
    ParticleEffectType.ENEMY_ATTACK_START: [
        AnimationFrame((7, 10)),
        AnimationFrame((7, 9)),
    ],
}
set_lengths_according_to_fps(PARTICLE_REGISTRY[ParticleEffectType.JUMP_DUST], seconds=0.3)
set_offset(PARTICLE_REGISTRY[ParticleEffectType.JUMP_DUST], offset=(0,2))
set_lengths_according_to_fps(PARTICLE_REGISTRY[ParticleEffectType.LAND_DUST], seconds=0.3)
set_lengths_according_to_fps(PARTICLE_REGISTRY[ParticleEffectType.BREAK], seconds=0.2)

set_lengths_according_to_fps(PARTICLE_REGISTRY[ParticleEffectType.ENEMY_ATTACK_START], seconds=0.2)


GENERIC_DEATH_ANIMATION = [
    AnimationFrame(pos=GDAE.DEATH_1.value),
    AnimationFrame(pos=GDAE.DEATH_2.value),
    AnimationFrame(pos=GDAE.DEATH_3.value),
    AnimationFrame(pos=GDAE.DEATH_4.value),
    AnimationFrame(pos=GDAE.DEATH_5.value),
    AnimationFrame(pos=GDAE.DEATH_6.value)
]
set_lengths_according_to_fps(GENERIC_DEATH_ANIMATION, seconds=0.5)


DEATH_ANIMATION_REGISTRY = {
        DEATH_ANIMATION_TYPE.PLAYER_HEART_SHATTER:
        [
         AnimationFrame(pos=(7,11)),
            AnimationFrame(pos=(7,12)),
            AnimationFrame(pos=(8,12)),
            AnimationFrame(pos=(8,13)),
        ],
        DEATH_ANIMATION_TYPE.DEFAULT_DEATH: GENERIC_DEATH_ANIMATION


}
set_lengths_according_to_fps(DEATH_ANIMATION_REGISTRY[DEATH_ANIMATION_TYPE.PLAYER_HEART_SHATTER], seconds=1)
set_offset(DEATH_ANIMATION_REGISTRY[DEATH_ANIMATION_TYPE.PLAYER_HEART_SHATTER], offset=(0,-8))

EFFECTS_REGISTRY = {
    EffectType.PARTICLE: PARTICLE_REGISTRY,
    EffectType.DEATH_ANIMATION: DEATH_ANIMATION_REGISTRY
}
