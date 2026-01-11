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

class AudioCommand(Command):
    def __init__(self, name="AudioCommand"):
        super().__init__(name=name)

class SoundCommand(AudioCommand):
    def __init__(self, sound_enum, loop=False):
        super().__init__(name="SoundCommand")
        self.sound_enum = sound_enum
        self.loop = loop

class MusicCommand(AudioCommand):
    def __init__(self, music_enum, loop=True, priority=0):
        super().__init__(name="MusicCommand")
        self.music_enum = music_enum
        self.loop = loop
        self.priority = priority

class PhysicsCommand(Command):
    def __init__(self, name="PhysicsCommand"):
        super().__init__(name=name)

class CollisionCommand(Command):
    def __init__(self, load: bool = True):
        super().__init__(name="CollisionCommand")
        self.load = load

class LoadEntityCollisionCommand(CollisionCommand):
    def __init__(self, load=True, entity=None):
        super().__init__(load=load)
        self.name = "LoadEntityCollisionCommand"
        self.entity = entity

class LoadMultipleEntityCollisionCommand(CollisionCommand):
    def __init__(self, load=True, entities=[]):
        super().__init__(load=load)
        self.name = "LoadMultipleEntityCollisionCommand"
        self.entities = entities
class LoadActiveAttackCollisionCommand(CollisionCommand):
    def __init__(self, load=True, attacking_entity=None):
        super().__init__(load=load)
        self.name = "LoadActiveAttackCollisionCommand"
        self.attacking_entity = attacking_entity
        # this actually uses the attacking entity to get the active attack hitbox and position, because the entity is used in the calculations and passed for the event. It's useful when determining direction of knockback and such
class LoadMultipleBoundariesCollisionCommand(CollisionCommand):
    def __init__(self, load=True, boundaries=[]):
        super().__init__(load=load)
        self.name = "LoadMultipleBoundariesCollisionCommand"
        self.boundaries = boundaries

class CombatCommand(Command):
    def __init__(self, origin, target, damage_amount, knockback=8, name="CombatCommand"):
        super().__init__(name=name)
        self.origin = origin
        self.target = target
        self.damage_amount = damage_amount
        self.knockback = knockback

class DamageCommand(CombatCommand):
    def __init__(self, origin, target, damage_amount, knockback=8):
        super().__init__(origin, target, damage_amount, knockback=knockback, name="DammageCommand")

# Need:
# commands will typically be issued to one manager
# CollisionLoad Commands, with load/unload, cell positions not needed
# Physics Commands, Add Momentum, Separate Momentum
# Damage Command (to tell damage manager to apply damage)
# Audio Command (to tell sound manager to play sound)

# types of managers:
# entity manager
# effects manager
# damage manager
# collision manager
# sound effects manager
# physics manager (held by entity manager, various types of physics managers depending on enemy type)


# notify_command must be held by managers to receive commands to act upon during their secondary update cycle, basically they receive it, store it, then act upon it later
class PhysicsCommand(Command):
    def __init__(self, name="PhysicsCommand"):
        super().__init__(name=name)


class AddMomentumCommand(PhysicsCommand):
    def __init__(self, entity, momentum_vector: list):
        super().__init__(name="AddMomentumCommand")
        self.entity = entity
        self.momentum_vector = momentum_vector

class EntitySeparationCommand(PhysicsCommand):
    def __init__(self, entity_a, entity_b, b_only=False):
        super().__init__(name="EntitySeparationCommand")
        self.entity = entity_a
        self.entity_b = entity_b
        self.b_only = b_only  # if true, only move entity b, else move both away from each other equally

class HUDCommand(Command):
    def __init__(self, name="HUDCommand"):
        super().__init__(name=name)

class TemporaryMessageCommand(HUDCommand):
    def __init__(self, message: str, seconds_duration: float = 2.0):
        super().__init__(name="TemporaryMessageCommand")
        self.message = message
        self.seconds_duration = seconds_duration

class DefenseCommand(Command):
    def __init__(self):
        super().__init__(name="DefenseCommand")

class StartBlockCommand(DefenseCommand):
    def __init__(self):
        super().__init__()
        self.name = "StartBlockCommand"

class EndBlockCommand(DefenseCommand):
    def __init__(self):
        super().__init__()
        self.name = "EndBlockCommand"

class BreakBlockCommand(DefenseCommand):
    def __init__(self):
        super().__init__()
        self.name = "BreakBlockCommand"
        # for when shield breaks

class ShieldHitCommand(CombatCommand):
    def __init__(self, origin, target, damage_amount, knockback=0):
        super().__init__(origin, target, damage_amount, knockback=knockback, name="ShieldHitCommand")
