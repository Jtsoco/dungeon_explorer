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
        AF(pos=(5,9), duration=6),
        AF(pos=(6,9), duration=6),
    ],
    SHIELD_ACTION_STATE.INVENTORY: [
        AF(pos=(5,6), duration=12)
    ]

}

set_lengths_according_to_fps(IRON_SHIELD, .3)
IRON_SHIELD[SHIELD_ACTION_STATE.TO_REST] = list(reversed(IRON_SHIELD[SHIELD_ACTION_STATE.TO_BLOCK].copy()))


DAGGER = {
    SHIELD_ACTION_STATE.IDLE: [AF(pos=(8,8), duration=12)],
    SHIELD_ACTION_STATE.TO_BLOCK: [
        AF(pos=(9,8), duration=1),
        AF(pos=(8,9), duration=2),
    ],
    SHIELD_ACTION_STATE.BLOCK: [
                                AF(pos=(9,9), duration=10),

                            ],
    SHIELD_ACTION_STATE.TO_REST: [
        AF(pos=(8,10), duration=1),
        # AF(pos=(9,10), duration=1),
        AF(pos=(5,6), duration=1),
    ],
    SHIELD_ACTION_STATE.BROKEN: [
        AF(pos=(8,11), duration=6),
        AF(pos=(9,11), duration=6),
    ],
    SHIELD_ACTION_STATE.INVENTORY: [
        AF(pos=(10,9), duration=12)
    ]
}

TOWER = {
    SHIELD_ACTION_STATE.IDLE: [
        AF(pos=(6,13), duration=12)
    ],
    SHIELD_ACTION_STATE.TO_BLOCK: [
        AF(pos=(7,13), duration=5),
        AF(pos=(6,14), duration=1),
        AF(pos=(7,14), duration=1),
        AF(pos=(6,15), duration=3),
    ],
    SHIELD_ACTION_STATE.BLOCK: [
        AF(pos=(7,15), duration=12)
    ],

    SHIELD_ACTION_STATE.BROKEN: [
        AF(pos=(6,16), duration=6),
        AF(pos=(7,16), duration=6),
    ],
    SHIELD_ACTION_STATE.INVENTORY: [
        AF(pos=(6,13), duration=12)
    ]

}
TOWER[SHIELD_ACTION_STATE.TO_REST] = list(reversed(TOWER[SHIELD_ACTION_STATE.TO_BLOCK].copy()))

SHIELD_ANIMATIONS = {
    SHIELD_CATEGORY.IRON_SHIELD: IRON_SHIELD,
    SHIELD_CATEGORY.DAGGER: DAGGER,
    SHIELD_CATEGORY.TOWER: TOWER


}

SHIELD_HITBOXES = {
    SHIELD_CATEGORY.IRON_SHIELD: {
        (4, 4)
        # hitbox size when blocking
        # if enemy attack attacks in direction shield faces, and hits shield, it's a block
    },
    SHIELD_CATEGORY.DAGGER: {
        (4,4)
    },
    SHIELD_CATEGORY.TOWER: {
        (6,6)
    }

}


SHIELD_STATS = {
    SHIELD_CATEGORY.IRON_SHIELD: {
        "max_stamina": 100,
        "drain_resistance": 25,
        "damage_resist": 1.0,
        "regen_delay": 20,
        "regen_amount": 10
    },
    SHIELD_CATEGORY.DAGGER: {
        "max_stamina": 50,
        "drain_resistance": 10,
        "damage_resist": 0.5,
        "regen_delay": 2,
        "regen_amount": 25
    },
    SHIELD_CATEGORY.TOWER: {
        "max_stamina": 500,
        "drain_resistance": 40,
        "damage_resist": 1.5,
        "regen_delay": 30,
        "regen_amount": 25
    }
}
