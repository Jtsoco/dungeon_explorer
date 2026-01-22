from enums.entity_enums import DirectionState as DS, MovementState as MS, InputEnums as IE, CollisionEntityTarget as CET

class Event():
    def __init__(self, name: str = "GenericEvent"):
        self.name = name

    def __str__(self):
        return f"Event: {self.name}"
class StateChangedEvent(Event):

    def __init__(self):
        super().__init__(name="StateChangedEvent")

class StateUpdateEvent(Event):
    def __init__(self, name="StateUpdateEvent"):
        super().__init__(name)

class InputEvent(Event):

    def __init__(self, input_type: IE, direction: DS = None):
        super().__init__(name="InputEvent")
        self.input_type = input_type
        self.direction = direction
        # MOVE events will have direction set to DS.LEFT or DS.RIGHT

    def __str__(self):
        return f"InputEvent: {self.input_type}"

class MovementEvent(StateUpdateEvent):
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



class AttackFinishedEvent(StateUpdateEvent):
    def __init__(self, name="AttackFinishedEvent"):
        super().__init__(name)

class BlockFinishedEvent(StateUpdateEvent):
    def __init__(self, name="BlockFinishedEvent"):
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
        # quick fix, edit later
        self.entity = entity_a
        # end quick fix
        self.entity_a = entity_a
        self.entity_b = entity_b

class DeathEvent(Event):
    def __init__(self, entity):
        super().__init__(name="DeathEvent")
        self.entity = entity

class BossDeathEvent(DeathEvent):
    def __init__(self, entity):
        super().__init__(entity)
        self.name = "BossDeathEvent"

class AddMomentumEvent(PhysicsEvent):
    def __init__(self, entity, momentum_vector: list):
        super().__init__(name="AddMomentumEvent")
        self.entity = entity
        self.momentum_vector = momentum_vector

class BoundaryCollisionEvent(Event):
    def __init__(self, entity, boundary):
        super().__init__(name="BoundaryCollisionEvent")
        self.entity = entity
        self.boundary = boundary

class CellEvent(Event):
    def __init__(self, name="CellEvent"):
        super().__init__(name)

class NewlyLoadedCellsEvent(CellEvent):
    def __init__(self, loaded_cells: list):
        super().__init__(name="NewlyLoadedCellsEvent")
        self.loaded_cells = loaded_cells

class PlayerEvent(Event):
    # this is specifically for events that happened to the player reported through the bus,
    def __init__(self, name="PlayerEvent"):
        super().__init__(name=name)

class PlayerDamagedEvent(PlayerEvent):
    def __init__(self, damage_amount):
        super().__init__(name="PlayerDamagedEvent")
        self.damage_amount = damage_amount

class PlayerHealedEvent(PlayerEvent):
    def __init__(self, heal_amount):
        super().__init__(name="PlayerHealedEvent")
        self.heal_amount = heal_amount

class PlayerShieldDamagedEvent(PlayerEvent):
    def __init__(self, damage_amount):
        super().__init__(name="PlayerShieldDamagedEvent")
        self.damage_amount = damage_amount

class PlayerDeathEvent(PlayerEvent):
    def __init__(self):
        super().__init__(name="PlayerDeathEvent")

class ActionFailedEvent(StateUpdateEvent):
    # useful when block or attack fails, for local entity loop
    def __init__(self, action_type=None):
        super().__init__(name="ActionFailedEvent")
        self.action_name = action_type
# Need:
# events will typically be things that happen in which multiple other systems may need to respond to
# World Event?
# Entity Events? Death event, Spawn Event, Despawn Event
# Combat Events? Damage Event, Heal Event, such as Damage Event notifying gui of player damage and need for update


# types of managers:
# entity manager
# effects manager
# damage manager
# collision manager
# sound effects manager
# physics manager (held by entity manager, various types of physics managers depending on enemy type)


# notify_event must be held by managers to receive events to act upon during their secondary update cycle, basically they receive it, store it, then act upon it later

class GameEvent(Event):
    def __init__(self, name="GameEvent"):
        super().__init__(name=name)

class GameOverEvent(GameEvent):
    def __init__(self):
        super().__init__(name="GameOverEvent")

class GameClearEvent(GameEvent):
    def __init__(self):
        super().__init__(name="GameClearEvent")
