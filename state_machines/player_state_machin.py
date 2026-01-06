from state_machines.default_state_machine import DefaultStateMachine
from enums.entity_enums import MovementState as MS, ActionState as AS, PowerUpStates as PUS
class PlayerStateMachine(DefaultStateMachine):
    def __init__(self):
        super().__init__()
        components = {}


class JumpComponent():
    def __init__(self):
        pass

    def action(self, data):
        match data.movement_state:
            case MS.IDLE | MS.WALKING:
                data.movement_state = MS.JUMPING
                return True
            case MS.JUMPING | MS.FALLING:
                # already jumping or falling, can't jump again
                return False

class DoubleJumpComponent():
    def __init__(self):
        pass

    def action(self, data):
        match data.movement_state:
            case MS.IDLE | MS.WALKING:
                data.movement_state = MS.JUMPING
                self.used_double_jump = False
                return True
            case MS.JUMPING| MS.FALLING:
                if self.can_double_jump(data):

                    data.movement_state = MS.JUMPING
                    self.used_double_jump = True
                    return True

    def can_double_jump(self, data):
        if data.powerup_states.get(PUS.DOUBLE_JUMP) is None:
            return False
        else:
            # it keeps track of whether it is used or not
            return data.powerup_states[PUS.DOUBLE_JUMP]
