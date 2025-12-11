from animations.animation_setup import animation_setup
from enums.entity_enums import MovementState as MS, DirectionState as DS, ActionState as AS
from attack.weapon_data import WeaponData

class AnimationData():
    def __init__(self, animation_setup=animation_setup()):
        self.current_frame = 0
        self.frame_timer = 0
        self.animations = animation_setup
        self.current_animation = self.animations[MS.IDLE]
    # the update handles frame duration, and is called by
    def get_current_frame(self):
        return self.current_animation[self.current_frame]
