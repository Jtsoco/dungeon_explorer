from enums.entity_enums import SHIELD_ACTION_STATE, SHIELD_CATEGORY
from animations.animation_frame import AnimationFrame as AF
from animations.frame_module import set_lengths_according_to_fps
IRON_SHIELD = {
    SHIELD_ACTION_STATE.IDLE: [
        AF(pos=(5,6), duration=12)
    ],
    SHIELD_ACTION_STATE.TO_BLOCK: [
        AF(pos=(6,6), duration=1),
        AF(pos=(5,7), duration=1),
        AF(pos=(6,7), duration=1),
        AF(pos=(5,8), duration=1),
    ],
    SHIELD_ACTION_STATE.BLOCK: [
        AF(pos=(6,8), duration=12)
    ],
    SHIELD_ACTION_STATE.BROKEN: [
        AF(pos=(5,10), duration=6),
        AF(pos=(6,10), duration=6),
    ]

}

set_lengths_according_to_fps(IRON_SHIELD, .3)
IRON_SHIELD[SHIELD_ACTION_STATE.TO_REST] = list(reversed(IRON_SHIELD[SHIELD_ACTION_STATE.TO_BLOCK].copy()))

SHIELD_ANIMATIONS = {
    SHIELD_CATEGORY.IRON_SHIELD: IRON_SHIELD
}

SHIELD_HITBOXES = {
    SHIELD_CATEGORY.IRON_SHIELD: {
        (4, 4)
        # hitbox size when blocking
        # if enemy attack attacks in direction shield faces, and hits shield, it's a block
    }
}

SHIELD_STATS = {
    SHIELD_CATEGORY.IRON_SHIELD: {
        "max_stamina": 100,
        "drain_resistance": 25,
        "damage_resist": 1.0
    }
}
