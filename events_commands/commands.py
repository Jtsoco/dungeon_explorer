from enums.entity_enums import DirectionState as DS
from enums.effects_enums import ParticleEffectType as PET, EffectType

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


class EffectCommand(Command):
    def __init__(self, pos=(0,0), sub_type=PET.JUMP_DUST, effect_type=EffectType.PARTICLE):
        super().__init__(name="EffectCommand")
        self.position = pos
        self.sub_type = sub_type
        self.effect_type = effect_type
