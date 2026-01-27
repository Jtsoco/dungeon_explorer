from enums.entity_enums import MovementState as MS, EntityType as ET, ActionState as AS
from animations.animation_enums import PlayerAnimationEnums as PAE, SkullAnimationEnums as SAE
from animations.animation_frame import AnimationFrame as AF

# NOTE: offsets:
        # the offset here is for weapon gripping point
        # basically offset is for where you want to hold something on a sprite,
        # but for a weapon it represents where the handle is drawn relative to the top left of its brick tile
player_offset = (7, 5)
ronin_offset = (7, 6)

# possibly refactor later so players and enemies have their own sprite registries, and if it expands to other dungeons separate enemy registries by dungeons so not all loaded at once, or maybe types of enemies for separation criteria
SPRITES = {

    ET.PLAYER: {
        MS.IDLE: [AF(offset=player_offset, pos=PAE.PLAYER_IDLE_1.value, duration=12)],
        MS.WALKING: [
            AF(offset=player_offset, pos=PAE.PLAYER_WALK_1.value, duration=6),
            AF(offset=player_offset, pos=PAE.PLAYER_WALK_2.value, duration=6)
        ],
        MS.JUMPING: [AF(offset=player_offset, pos=PAE.PLAYER_JUMP.value, duration=12)],
        MS.FALLING: [AF(offset=player_offset, pos=PAE.PLAYER_FALL.value, duration=12)],
    },
    ET.PLAYER_RONIN: {
        MS.IDLE: [AF(offset=ronin_offset, pos=PAE.RONIN_IDLE.value, duration=12)],
        MS.WALKING: [
            AF(offset=ronin_offset, pos=PAE.RONIN_WALK_1.value, duration=6),
            AF(offset=ronin_offset, pos=PAE.RONIN_WALK_2.value, duration=6)
        ],
        MS.JUMPING: [AF(offset=ronin_offset, pos=PAE.RONIN_JUMP.value, duration=12)],
        MS.FALLING: [AF(offset=ronin_offset, pos=PAE.RONIN_FALL.value, duration=12)],
    },

    ET.SKULL: {
        MS.IDLE: [AF(pos=SAE.SKULL_IDLE_1.value, duration=12)],
        MS.WALKING: [
            AF(pos=SAE.SKULL_WALK_1.value, duration=6),
            AF(pos=SAE.SKULL_WALK_2.value, duration=6)
        ]
    },

    ET.KNIGHT: {
        MS.IDLE:
            [
                AF(
                pos=(0,16), duration=12, offset=player_offset)
            ],
        MS.WALKING: [
            AF(pos=(0,17), duration=6, offset=player_offset),
            AF(pos=(1,17), duration=6, offset=player_offset)
        ]
    }


}

BOSS_SPRITES = {
    ET.WINGED_KNIGHT: {
        MS.IDLE:
        [
            AF(
            pos=(0,23), duration=12, offset=player_offset)
        ],
        MS.WALKING: [
            AF(pos=(0,24), duration=6, offset=player_offset),
            AF(pos=(1,24), duration=6, offset=player_offset)
        ],
        MS.JUMPING: [
            AF(pos=(0,25), duration=12, offset=player_offset)
        ],
        MS.FALLING: [
            AF(pos=(0,25), duration=12, offset=player_offset)
        ]
    },
    ET.DARK_LORD: {
        MS.IDLE:
        [
            AF(
            pos=(7,26), duration=12, offset=(12, -1), w_h=(8,16))
        ],
        MS.WALKING: [
            AF(pos=(8,28), duration=6, offset=(12, -1), w_h=(8,16)),
            AF(pos=(9,28), duration=6, offset=(12, -1), w_h=(8,16)),
            AF(pos=(10,28), duration=6, offset=(12, -1), w_h=(8,16)),
        ],
        MS.JUMPING: [
            AF(pos=(6,28), duration=12, offset=(12, -1), w_h=(8,16))
        ],
        MS.FALLING: [
            AF(pos=(6,28), duration=12, offset=(12, -1), w_h=(8,16))
        ],
        AS.ATTACKING: [
            AF(pos=(7,28), duration=4, offset=(16, -1), w_h=(8,16)),
        ]

    }
}
