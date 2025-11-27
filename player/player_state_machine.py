from player_enums import MovementState as MS, ActionState as AS, DirectionState as DS, InputEvents as IE
from ..events_commands.events import InputEvent
from ..events_commands.commands import MoveCommand, JumpCommand
class PlayerStateMachine():
    def __init__(self):
        self.events = []

    # in here is the logic to determine what the next state is based on the previous

    def input_events(self, data, input_events):
        # will it set the data to hold state of moving/idle, or let something else handle that?
        # it may be fine if it only changes that state, but it may be important to only let it do that once during a loop
        # then again it only gets the input events once, need to think about this more
        return_events = []
        return_commands = []
        return_items = (return_events, return_commands)
        for event in input_events:
            if event.input_type == IE.MOVE:
                command = self.set_walking(data, event.direction)
                return_commands.append(command)
            elif event.input_type == IE.STOP_MOVE:
                command = self.stop_move(data)
                return_commands.append(command)


    def set_walking(self, data, event_type):
        # this will eventually decide
        data.movement_state = MS.WALKING
        # event type is DS.LEFT or DS.RIGHT
        data.direction_state = event_type
        return MoveCommand(event_type)

    def stop_move(self, data):
        data.movement_state = MS.IDLE
        return MoveCommand(DS.HALT)
