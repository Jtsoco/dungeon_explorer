
from enums.entity_enums import MovementState as MS, EntityType as ET
from animations.sprite_registry import SPRITES

class AnimationData():
    def __init__(self, animation_setup=SPRITES[ET.PLAYER]):
        self.current_frame = 0
        self.frame_timer = 0
        self.animations = animation_setup
        self.current_animation = self.animations[MS.IDLE]
    # the update handles frame duration, and is called by
    def get_current_frame(self):
        return self.current_animation[self.current_frame]
