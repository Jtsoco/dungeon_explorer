from animations.animation_enums import GenericDeathAnimationEnums as GDAE
from animations.animation_frame import AnimationFrame as AF
from animations.frame_module import set_lengths_according_to_fps



GENERIC_DEATH_ANIMATION = [
    AF(pos=GDAE.DEATH_1.value),
    AF(pos=GDAE.DEATH_2.value),
    AF(pos=GDAE.DEATH_3.value),
    AF(pos=GDAE.DEATH_4.value),
    AF(pos=GDAE.DEATH_5.value),
    AF(pos=GDAE.DEATH_6.value)
]

set_lengths_according_to_fps(GENERIC_DEATH_ANIMATION, seconds=0.5)  # half a second death animation
