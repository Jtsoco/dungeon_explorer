from player.player_enums import MovementState as MS, DirectionState as DS, ActionState as AS

class PlayerData():
    def __init__(self):
        self.position = [0, 0]
        self.w_h = (8, 6)
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
