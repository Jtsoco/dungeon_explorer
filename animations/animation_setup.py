from enums.entity_enums import HorizontalMovementState as HMS, VerticalMovementState as VMS, DirectionState as DS, ActionState as AS, WeaponActionState as WAS
from animations.animation_enums import PlayerAnimationEnums as PAE

class AnimationFrame():
    def __init__(self, pos: tuple, duration: int=6, offset: tuple=(0,0)):
        self.pos = pos
        self.duration = duration
        self.offset = offset

def animation_setup():
    # for regular offset, it will refer to where the hands are drawn relative to the top left of its brick tile
    animations = {}
    offset = (7,5)
    animations[HMS.IDLE] = [AnimationFrame(PAE.PLAYER_IDLE_1.value, duration=12, offset=offset),]

    animations[HMS.WALKING] = [
        AnimationFrame(PAE.PLAYER_WALK_1.value, duration=6, offset=offset),
        AnimationFrame(PAE.PLAYER_WALK_2.value, duration=6, offset=offset)
    ]
    offset = (7, 5)
    animations[VMS.JUMPING] = [AnimationFrame(PAE.PLAYER_JUMP.value, duration=12, offset=offset),]
    offset = (7,5)
    animations[VMS.FALLING] = [AnimationFrame(PAE.PLAYER_FALL.value, duration=12, offset=offset),]

    return animations
# return a dict of animations using some predefined setup


def default_attack_animation():
    animations = {}
    offset = (0, 6)
    default_sheathed = AnimationFrame((2, 6), duration=3, offset=offset)
    sheathed = [
        default_sheathed
    ]
    # offset refers to where the weapon handle is drawn relative to the top left of its brick tile
    offset = (1, 5)
    attack_animation = [
        default_sheathed,
        AnimationFrame((3, 6), duration=1, offset=offset ),
        AnimationFrame((2, 7), duration=1, offset=offset ),
        AnimationFrame((3, 7), duration=11, offset=offset ),
    ]
    animations[WAS.SHEATHED] = sheathed
    animations[WAS.DEFAULT] = attack_animation
    return animations

def skull_animation():
    animations = {}
    animations[HMS.IDLE] = [AnimationFrame((0, 15), duration=12)]
    animations[HMS.WALKING] = [
        AnimationFrame((0, 15), duration=6),
        AnimationFrame((1, 15), duration=6)
    ]
    return animations
