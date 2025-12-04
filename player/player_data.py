from player.player_enums import MovementState as MS, DirectionState as DS, ActionState as AS


from player.animations.animation_setup import animation_setup

class AnimationData():
    def __init__(self):
        self.current_frame = 0
        self.frame_timer = 0
        self.animations = animation_setup()
        self.last_frame = self.animations[MS.IDLE][-1]
    # the update handles frame duration, and is called by

class PlayerData():
    def __init__(self):
        self.position = [0, 0]
        self.w_h = (8, 8)
        # width and height for now, revisit values later

        self.costume = "default"
        self.movement_state = MS.IDLE
        self.last_movement_input = None
        self.direction_state = DS.RIGHT
        self.action_state = AS.NONE


        self.move_speed = 2
        self.jump_strength = 3
        # need to do some serious refactor on physics values and gravity later


        self.velocity = [0, 0]

        self.animation_data = AnimationData()
