from enums.entity_enums import MovementState as MS, ActionState as AS, DirectionState as DS, InputEnums as IE, PowerUpStates as PUS
from events_commands.events import InputEvent, StartedFallingEvent, LandedEvent, StateChangedEvent, AttackFinishedEvent
from events_commands.commands import MoveCommand, JumpCommand, AttackCommand
class DefaultStateMachine():
    def __init__(self):
        self.events = []

    # in here is the logic to determine what the next state is based on the previous

    def input_events(self, data, input_events):
        # will it set the data to hold state of moving/idle, or let something else handle that?
        # it may be fine if it only changes that state, but it may be important to only let it do that once during a loop
        # then again it only gets the input events once, need to think about this more
        last_states = [data.movement_state, data.action_state, data.direction_state]

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

        new_states = [data.movement_state, data.action_state, data.direction_state]
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
        match data.movement_state:
            case MS.IDLE | MS.WALKING:
                data.movement_state = MS.JUMPING
                return JumpCommand()
            case MS.JUMPING | MS.FALLING:
                if self.can_double_jump(data):
                    data.movement_state = MS.JUMPING
                    return JumpCommand()
                return None

    def can_double_jump(self, data):
        if PUS.DOUBLE_JUMP in data.power_ups:
            if data.power_ups[PUS.DOUBLE_JUMP]:
                data.power_ups[PUS.DOUBLE_JUMP] = False  # mark as used
                return True

        return False

    def set_walking(self, data, event_type):
        # this will eventually decide
        match data.movement_state:
            case MS.IDLE:
                data.movement_state = MS.WALKING
        # event type is DS.LEFT or DS.RIGHT
        data.direction_state = event_type
        return MoveCommand(event_type)

    def stop_move(self, data):
        match data.movement_state:
            case MS.WALKING:
                data.movement_state = MS.IDLE
        return MoveCommand(DS.HALT)

    def state_updates(self, data, updates):
        last_states = [data.movement_state, data.action_state, data.direction_state]
        for event in updates:
            match event:
                case StartedFallingEvent():
                    data.movement_state = MS.FALLING
                case LandedEvent():
                    data.movement_state = MS.IDLE
                    if PUS.DOUBLE_JUMP in data.power_ups:
                        data.power_ups[PUS.DOUBLE_JUMP] = True  # reset double jump on land
                case AttackFinishedEvent():
                    data.action_state = AS.NONE
        new_states = [data.movement_state, data.action_state, data.direction_state]
        if new_states != last_states:
            return StateChangedEvent()
