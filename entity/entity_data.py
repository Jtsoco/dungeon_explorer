# basic entity data
from enums.entity_enums import MovementState as MS, DirectionState as DS, ActionState as AS, EntityType as ET
# make an enemy type enum, and use composition for enemy behaviors/ things later
from entity.animation_data import AnimationData

class EntityData():
    def __init__(self, position: list = [0, 0], w_h: tuple = (8, 8), animation_data=AnimationData(), weapon_data = None, entity_type=ET.KNIGHT):
        self.position = position  # (x, y)
        self.w_h = w_h  # (width, height)
        self.entity_type = entity_type

        self.animation_data = animation_data
        self.movement_state = MS.IDLE
        self.direction_state = DS.RIGHT
        self.action_state = AS.NONE

        self.weapon = weapon_data

        self.velocity = [0, 0]  # (x_velocity, y_velocity)

        self.move_speed = 2

        self.jump_strength = 3

        # for now, just a simple thing to keep track of how long it has been in a decision state, for simple AI
        self.state_timer = 0
        self.frame_rate = 30  # default frame rate, can be changed later
