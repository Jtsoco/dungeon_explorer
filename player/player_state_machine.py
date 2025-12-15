from enums.entity_enums import HorizontalMovementState as HMS, VerticalMovementState as VMS, ActionState as AS, DirectionState as DS, InputEnums as IE
from events_commands.events import InputEvent, StartedFallingEvent, LandedEvent, StateChangedEvent, AttackFinishedEvent
from events_commands.commands import MoveCommand, JumpCommand, AttackCommand
class PlayerStateMachine():
    def __init__(self):
        self.events = []

    # in here is the logic to determine what the next state is based on the previous

    def input_events(self, data, input_events):
        # will it set the data to hold state of moving/idle, or let something else handle that?
        # it may be fine if it only changes that state, but it may be important to only let it do that once during a loop
        # then again it only gets the input events once, need to think about this more
        last_states = [data.h_movement_state, data.v_movement_state, data.action_state, data.direction_state]

        return_events = []
        return_commands = []
        return_items = (return_events, return_commands)
        for event in input_events:
            match event.input_type:
                case IE.MOVE:
                    command = self.set_walking(data, event.direction)
                    return_commands.append(command)
                case IE.STOP_MOVE:
                    command = self.stop_move(data)
                    return_commands.append(command)
                case IE.JUMP:
                    command = self.jump_input(data)
                    if command:
                        return_commands.append(command)
                case IE.ATTACK:
                    command = self.attack_input(data)
                    if command:
                        return_commands.append(command)

        new_states = [data.h_movement_state, data.v_movement_state, data.action_state, data.direction_state]
        if new_states != last_states:
            return_events.append(StateChangedEvent())
        return return_items

    def attack_input(self, data):
        match data.action_state:
            case AS.NONE:
                data.action_state = AS.ATTACKING
                return AttackCommand()
            case _:
                return None

    def jump_input(self, data):
        match data.v_movement_state:
            case VMS.STANDING:
                data.vertical_movement_state = VMS.JUMPING
                return JumpCommand()
            case VMS.JUMPING | VMS.FALLING:
                # already jumping or falling, can't jump again
                return None

    def set_walking(self, data, event_type):
        # this will eventually decide
        match data.h_movement_state:
            case HMS.IDLE:
                data.h_movement_state = HMS.WALKING
        # event type is DS.LEFT or DS.RIGHT
        data.direction_state = event_type
        return MoveCommand(event_type)

    def stop_move(self, data):
        match data.h_movement_state:
            case HMS.WALKING:
                data.h_movement_state = HMS.IDLE
        return MoveCommand(DS.HALT)

    def state_updates(self, data, updates):
        last_states = [data.h_movement_state, data.v_movement_state,  data.action_state, data.direction_state]
        for event in updates:
            match event:
                case StartedFallingEvent():
                    data.v_movement_state = VMS.FALLING
                case LandedEvent():
                    data.v_movement_state = VMS.STANDING
                case AttackFinishedEvent():
                    data.action_state = AS.NONE
        new_states = [data.h_movement_state, data.v_movement_state, data.action_state, data.direction_state]
        if new_states != last_states:
            return StateChangedEvent()
