from animations.animation_enums import GenericDeathAnimationEnums as GDAE
from animations.animation_frame import AnimationFrame as AF
from magic_numbers import FPS

def set_lengths_according_to_fps(animation, seconds=1):
    length = (seconds * FPS) // len(animation)
    # just need a whole numebr
    for frame in animation:
        frame.duration = FPS // length
# for now fps are locked, but may change later, so will just do a quick for loop to set durations
# eventually will maybe want to change fps mid game, but for now this setup will work on restart/reload of modules

GENERIC_DEATH_ANIMATION = [
    AF(pos=GDAE.DEATH_1.value),
    AF(pos=GDAE.DEATH_2.value),
    AF(pos=GDAE.DEATH_3.value),
    AF(pos=GDAE.DEATH_4.value),
    AF(pos=GDAE.DEATH_5.value),
    AF(pos=GDAE.DEATH_6.value)
]

set_lengths_according_to_fps(GENERIC_DEATH_ANIMATION)
