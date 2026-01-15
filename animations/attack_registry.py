
from animations.animation_frame import AnimationFrame as AF
from enums.entity_enums import WeaponActionState as WAS, WeaponCategory as WC

WEAPONS_ANIMATIONS = {
    WC.SHORTSWORD: {
        WAS.SHEATHED: [AF(offset=(0, 6), pos=(2, 6), duration=3)],
        WAS.DEFAULT: [
            AF(offset=(0, 6), pos=(2, 6), duration=3),
            AF(offset=(1, 5), pos=(3, 6), duration=1),
            AF(offset=(1, 5), pos=(2, 7), duration=1),
            AF(offset=(1, 5), pos=(3, 7), duration=6),
        ],
        WAS.INVENTORY: [
            AF(offset=(0, 0), pos=(1, 8), duration=12)
        ]
    },
    WC.ENEMY_SWORD: {
        WAS.SHEATHED: [AF(offset=(0, 6), pos=(2, 6), duration=15)],
        WAS.DEFAULT: [
            AF(offset=(0, 6), pos=(2, 6), duration=15),
            AF(offset=(1, 5), pos=(3, 6), duration=1),
            AF(offset=(1, 5), pos=(2, 7), duration=1),
            AF(offset=(1, 5), pos=(3, 7), duration=6),
        ],
        WAS.INVENTORY: [
            AF(offset=(0, 0), pos=(2, 6), duration=12)
        ]
    },
    WC.KATANA: {
        WAS.SHEATHED: [AF(pos=(9,6), offset=(7,6), duration=3)],
        WAS.DEFAULT: [
            # AF(pos=(9,6), offset=(1,6), duration=1),
            AF(pos=(10,6), offset=(1,6), duration=1),
            AF(pos=(9,7), offset=(1,6), duration=1),
            AF(pos=(10,7), offset=(1,6), duration=1),
        ],
        WAS.INVENTORY: [
            AF(pos=(10,8), offset=(0,0), duration=12)
        ]
    },
    WC.GLAIVE: {
        WAS.SHEATHED: [AF(pos=(0,26), duration=10, offset=(6,14), w_h=(8, 16))],
        WAS.DEFAULT: [
            AF(pos=(0,26), duration=10, offset=(6,14), w_h=(8, 16)),
            AF(pos=(1,26), duration=1, offset=(5,13), w_h=(8, 16), rotation=30),
            AF(pos=(1,26), duration=1, offset=(4,12), w_h=(8, 16), rotation=60),
            AF(pos=(0,26), duration=11, offset=(3,11), w_h=(8, 16), rotation=90),
        ],
        WAS.AIRATTACK: [
            # honestly given the attack is spinning around, might be good to make a system to allow for a looping animation frame, that instead uses a duration to determine when to use the next rotation frame. For now, just use a bunch of AF instances, because it's quickest for this one attack
            AF(pos=(0,26), duration=10, offset=(6,12), w_h=(8, 16), rotation=0),
            # AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=0),
            AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=30),
            # AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=60),
            AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=90),
            # AF(pos=(0,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=120),
            AF(pos=(0,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=150),
            # AF(pos=(0,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=180),
            AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=210),
            # AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=240),
            AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=270),
            # AF(pos=(1,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=300),
            AF(pos=(0,26), duration=1, offset=(6,12), w_h=(8, 16), rotation=330),
        ],
        WAS.INVENTORY: [
            AF(pos=(2,27), duration=12, offset=(0,0), w_h=(8, 16))
        ]
    }

}


WEAPONS_HITBOXES = {
    WC.SHORTSWORD: {
        WAS.SHEATHED: {
            0: (0, 0)  # no hitbox when sheathed
        },
        WAS.DEFAULT: {
            0: (0, 0),  # no hitbox on first animation frame
            1: (8, 4),
            2: (8, 6),
            3: (8, 8),
        }
    },
    WC.ENEMY_SWORD: {
        WAS.SHEATHED: {
            0: (0, 0)  # no hitbox when sheathed
        },
        WAS.DEFAULT: {
            0: (0, 0),  # no hitbox on first animation frame
            1: (8, 4),
            2: (8, 6),
            3: (8, 8),
        }
    },
    WC.GLAIVE: {
        WAS.SHEATHED: {
            0: (0, 0)  # no hitbox when sheathed
        },
        WAS.DEFAULT: {
            0: (0, 0),  # no hitbox on first animation frame
            1: (7, 6),
            2: (7, 8),
            3: (7, 10),
        },
        WAS.AIRATTACK: {
            # revisit this later, just a quick implementation for now using ai autocomplete
            0: (3, 3),
            1: (7, 8),
            2: (7, 8),
            3: (7, 10),
            4: (5, 10),
            5: (4, 4),
            6: (4, 4),
            # 7: (8, 4),
            # 8: (10, 6),
            # 9: (12, 8),
            # 10: (14, 10),
            # 11: (14, 10),
        }
    },
    WC.KATANA: {
        WAS.SHEATHED: {
            0: (0, 0)  # no hitbox when sheathed
        },
        WAS.DEFAULT: {
            0: (0, 0),  # no hitbox on first animation frame
            1: (8, 6),
            2: (8, 6),
            3: (8, 6),
        }
    }


}

# honestly now that it's including stats should move this out of animations folder later
WEAPON_STATS = {
    WC.SHORTSWORD: {
        "damage": 50,
        "knockback": (1.5, 1)
    },
    WC.GLAIVE: {
        "damage": 80,
        "knockback": (2.0, 1.5)
    },
    WC.KATANA: {
        "damage": 50,
        "knockback": (.3, 0)
    },
    WC.ENEMY_SWORD: {
        "damage": 40,
        "knockback": (1.0, 0.5)
    },
}
