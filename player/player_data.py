from enums.entity_enums import HorizontalMovementState as HMS, VerticalMovementState as VMS, DirectionState as DS, ActionState as AS, EntityCategory as EC, EntityType as ET


from animations.animation_setup import animation_setup
from attack.weapon_data import WeaponData
class AnimationData():
    def __init__(self, animation_setup=animation_setup()):
        self.current_frame = 0
        self.frame_timer = 0
        self.animations = animation_setup
        self.current_animation = self.animations[HMS.IDLE]
    # the update handles frame duration, and is called by
    def get_current_frame(self):
        return self.current_animation[self.current_frame]

class PlayerData():
    def __init__(self):
        # refactor this to be derived from entity data later
        self.health = 100
        self.position = [0, 0]
        self.w_h = (8, 8)
        # width and height for now, revisit values later

        self.costume = "default"
        self.h_movement_state = HMS.IDLE
        self.v_movement_state = VMS.STANDING
        self.last_movement_input = None
        self.direction_state = DS.RIGHT
        self.action_state = AS.NONE
        self.player=True
        self.entity_category = EC.GROUND
        self.entity_type = ET.KNIGHT


        self.move_speed = 2
        self.jump_strength = 3
        # need to do some serious refactor on physics values and gravity later


        self.velocity = [0, 0]

        self.animation_data = AnimationData()

        self.weapon = WeaponData()
