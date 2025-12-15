# basic entity data
from enums.entity_enums import HorizontalMovementState as MS, VerticalMovementState as VMS, DirectionState as DS, ActionState as AS, EntityType as ET, EntityCategory as EC
# make an enemy type enum, and use composition for enemy behaviors/ things later
from entity.animation_data import AnimationData

class EntityData():
    def __init__(self, position: list = [0, 0], w_h: tuple = (8, 8), animation_data=AnimationData(), weapon_data = None, entity_type=ET.KNIGHT, entity_category=EC.GROUND, speed=1, cell_pos=(0,0), player=False, health=100, touch_damage=0):
        self.health = health
        self.player = player
        self.position = position  # (x, y)
        self.w_h = w_h  # (width, height)
        self.entity_type = entity_type
        self.entity_category = entity_category  # whether the entity is affected by gravity or not

        self.animation_data = animation_data
        self.h_movement_state = MS.IDLE
        self.v_movement_state = MS.STANDING
        self.direction_state = DS.RIGHT
        self.action_state = AS.NONE

        self.weapon = weapon_data

        self.velocity = [0, 0]  # (x_velocity, y_velocity)

        self.move_speed = speed

        self.jump_strength = 3



        # for now, just a simple thing to keep track of how long it has been in a decision state, for simple AI
        self.state_timer = 0
        self.frame_rate = 30  # default frame rate, can be changed later
        self.state_timer_limit = 60  # default time to wait before changing state, can be changed later

        self.cell_pos = cell_pos  # (cell_x_min, cell_y_min, cell_x_max, cell_y_max)

        self.touch_damage = touch_damage
