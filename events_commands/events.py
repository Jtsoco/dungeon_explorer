from player.player_enums import DirectionState as DS, MovementState as MS, InputEnums as IE

class Event():
    def __init__(self, name: str = "GenericEvent"):
        self.name = name

    def __str__(self):
        return f"Event: {self.name}"

class InputEvent(Event):

    def __init__(self, input_type: IE, direction: DS = None):
        super().__init__(name="InputEvent")
        self.input_type = input_type
        self.direction = direction
        # MOVE events will have direction set to DS.LEFT or DS.RIGHT

    def __str__(self):
        return f"InputEvent: {self.input_type}"
