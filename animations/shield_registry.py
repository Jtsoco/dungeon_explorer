from enums.entity_enums import SHIELD_ACTION_STATE, SHIELD_CATEGORY
from animations.animation_frame import AnimationFrame as AF
from animations.frame_module import set_lengths_according_to_fps
IRON_SHIELD = {
    SHIELD_ACTION_STATE.IDLE: [
        AF(pos=(5,6), duration=12)
    ],
    SHIELD_ACTION_STATE.TO_BLOCK: [
        AF(pos=(6,6), duration=3),
        AF(pos=(5,7), duration=3),
        AF(pos=(6,7), duration=3),
        AF(pos=(5,8), duration=3),
    ],
    SHIELD_ACTION_STATE.BLOCK: [
        AF(pos=(5,9), duration=12)
    ],

}
IRON_SHIELD = set_lengths_according_to_fps(IRON_SHIELD, .3)

IRON_SHIELD[SHIELD_ACTION_STATE.TO_REST] = list(reversed(IRON_SHIELD[SHIELD_ACTION_STATE.TO_BLOCK].copy().reverse()))

SHIELD_ANIMATIONS = {
    SHIELD_CATEGORY.IRON_SHIELD: IRON_SHIELD
}
