class Event():
    def __init__(self, name: str = "GenericEvent"):
        self.name = name

    def __str__(self):
        return f"Event: {self.name}"

class InputEvent(Event):

    def __init__(self, input_type: str):
        super().__init__(name="InputEvent")
        self.input_type = input_type

    def __str__(self):
        return f"InputEvent: {self.input_type}"
