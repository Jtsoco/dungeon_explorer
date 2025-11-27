from ..player.player_enums import DirectionState as DS

class Command():
    def __init__(self, name: str = "GenericCommand"):
        self.name = name

    def __str__(self):
        return f"Command: {self.name}"

class MoveCommand(Command):

    def __init__(self, direction: DS):
        super().__init__(name="MoveCommand")
        self.direction = direction

    def __str__(self):
        return f"MoveCommand: {self.direction}"

class JumpCommand(Command):

    def __init__(self):
        super().__init__(name="JumpCommand")
