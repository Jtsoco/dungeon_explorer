from animations.animation_frame import AnimationFrame as AF
from enums.entity_enums import WeaponActionState as WAS, WeaponCategory as WC

WEAPONS_ANIMATIONS = {
    WC.SHORTSWORD: {
        WAS.SHEATHED: [AF(offset=(0, 6), pos=(2, 6), duration=3)],
        WAS.DEFAULT: [
            AF(offset=(0, 6), pos=(2, 6), duration=3),
            AF(offset=(1, 5), pos=(3, 6), duration=1),
            AF(offset=(1, 5), pos=(2, 7), duration=1),
            AF(offset=(1, 5), pos=(3, 7), duration=11),
        ]
    }

}

WEAPONS_HITBOXES = {
    WC.SHORTSWORD: {
        WAS.DEFAULT: {
            0: (0, 0),  # no hitbox on first animation frame
            1: (8, 4),
            2: (8, 6),
            3: (8, 8),
        }
    }
}
