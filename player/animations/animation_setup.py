from player.player_enums import MovementState as MS, DirectionState as DS, ActionState as AS
from player.animations.animation_enums import PlayerAnimationEnums as PAE

class AnimationFrame():
    def __init__(self, pos: tuple, duration: int=6):
        self.pos = pos
        self.duration = duration

def animation_setup():
    animations = {}
    animations[MS.IDLE] = [AnimationFrame(PAE.PLAYER_IDLE_1.value, duration=12)]

    animations[MS.WALKING] = [
        AnimationFrame(PAE.PLAYER_WALK_1.value, duration=6),
        AnimationFrame(PAE.PLAYER_WALK_2.value, duration=6)
    ]
    animations[MS.JUMPING] = [AnimationFrame(PAE.PLAYER_JUMP.value, duration=12)]

    animations[MS.FALLING] = [AnimationFrame(PAE.PLAYER_FALL.value, duration=12)]

    return animations
# return a dict of animations using some predefined setup
