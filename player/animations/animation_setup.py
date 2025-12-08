from player.player_enums import MovementState as MS, DirectionState as DS, ActionState as AS, WeaponActionState as WAS
from player.animations.animation_enums import PlayerAnimationEnums as PAE

class AnimationFrame():
    def __init__(self, pos: tuple, duration: int=6, offset: tuple=(0,0)):
        self.pos = pos
        self.duration = duration
        self.offset = offset

def animation_setup():
    # for regular offset, it will refer to where the hands are drawn relative to the top left of its brick tile
    animations = {}
    offset = (7,5)
    animations[MS.IDLE] = [AnimationFrame(PAE.PLAYER_IDLE_1.value, duration=12, offset=offset),]

    animations[MS.WALKING] = [
        AnimationFrame(PAE.PLAYER_WALK_1.value, duration=6, offset=offset),
        AnimationFrame(PAE.PLAYER_WALK_2.value, duration=6, offset=offset)
    ]
    offset = (7, 1)
    animations[MS.JUMPING] = [AnimationFrame(PAE.PLAYER_JUMP.value, duration=12, offset=offset),]
    offset = (7,2)
    animations[MS.FALLING] = [AnimationFrame(PAE.PLAYER_FALL.value, duration=12, offset=offset),]

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
