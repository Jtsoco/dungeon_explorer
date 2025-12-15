from enums.entity_enums import DirectionState as DS, HorizontalMovementState as HMs, VerticalMovementState as VMS, InputEnums as IE, CollisionEntityTarget as CET

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

class PossibleCollisionEvent(Event):
    def __init__(self, origin=None, target_type = CET.ENEMY):
        super().__init__(name="PossibleCollisionEvent")
        self.origin = origin
        self.target_type = target_type

class PossibleAttackCollisionEvent(PossibleCollisionEvent):
    def __init__(self, origin, target_type = CET.ENEMY, attack_position= (0,0),):
        # in this instance, the attack is the origin, instance of a weapon data class
        # attack will carry an active hitbox
        super().__init__(origin, target_type)
        self.attack_position = attack_position
        self.name = "PossibleAttackCollisionEvent"



class DamageEvent(Event):
    def __init__(self, origin, target, damage_amount, knockback=8):
        # will possibly add knockback later, and origin will move from reference to id
        super().__init__(name="DamageEvent")
        self.origin = origin
        self.target = target
        self.damage_amount = damage_amount
        self.knockback = knockback


class PhysicsEvent(Event):
    def __init__(self, name="PhysicsEvent"):
        super().__init__(name)

class EntitySeparatedEvent(PhysicsEvent):
    def __init__(self, entity_a, entity_b):
        super().__init__(name="EntitySeparatedEvent")
        self.entity_a = entity_a
        self.entity_b = entity_b

class DeathEvent(Event):
    def __init__(self, entity):
        super().__init__(name="DeathEvent")
        self.entity = entity

class AddMomentumEvent(PhysicsEvent):
    def __init__(self, entity, momentum_vector: list):
        super().__init__(name="AddMomentumEvent")
        self.entity = entity
        self.momentum_vector = momentum_vector
