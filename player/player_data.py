from player_enums import MovementState as MS, DirectionState as DS, ActionState as AS

class PlayerData():
    def __init__(self):
        self.position = (0, 0)
        self.costume = "default"
        self.movement_state = MS.IDLE
        self.direction_state = DS.RIGHT
        self.action_state = AS.NONE
        self.velocity = (0, 0)
