from enums.entity_enums import DirectionState as DS

class Command():
    def __init__(self, name: str = "GenericCommand"):
        self.name = name

    def __str__(self):
        return f"Command: {self.name}"

class MovementCommand(Command):
    # commands for movement system
    pass


class MoveCommand(MovementCommand):

    def __init__(self, direction: DS = None):
        super().__init__(name="MoveCommand")
        self.direction = direction

    def __str__(self):
        return f"MoveCommand: {self.direction}"


class JumpCommand(MovementCommand):

    def __init__(self):
        super().__init__(name="JumpCommand")

class AttackCommand(Command):
    def __init__(self):
        super().__init__(name="AttackCommand")
