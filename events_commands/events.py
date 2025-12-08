from player.player_enums import DirectionState as DS, MovementState as MS, InputEnums as IE

class Event():
    def __init__(self, name: str = "GenericEvent"):
        self.name = name

    def __str__(self):
        return f"Event: {self.name}"
class StateChangedEvent(Event):

    def __init__(self):
        super().__init__(name="StateChangedEvent")


class InputEvent(Event):

    def __init__(self, input_type: IE, direction: DS = None):
        super().__init__(name="InputEvent")
        self.input_type = input_type
        self.direction = direction
        # MOVE events will have direction set to DS.LEFT or DS.RIGHT

    def __str__(self):
        return f"InputEvent: {self.input_type}"

class MovementEvent(Event):
    # events for movement system
    # indicating something movement related has happened
    def __init__(self, name="MovementEvent"):
        super().__init__(name)

class LandedEvent(MovementEvent):
    def __init__(self, name="LandedEvent"):
        super().__init__(name)



class StartedFallingEvent(MovementEvent):
    def __init__(self, name="StartedFallingEvent"):
        super().__init__(name)

class AttackFinishedEvent(Event):
    def __init__(self, name="AttackFinishedEvent"):
        super().__init__(name)
