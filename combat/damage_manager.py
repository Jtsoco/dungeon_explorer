from enums.entity_enums import DirectionState as DS
from events_commands.events import DeathEvent, AddMomentumEvent

class DamageManager():
    def __init__(self):
        pass

    # goal of this class as of now:
    # receive damage events, apply damage to entities, handle sending out any resulting events like dead events

    def handle_event(self, event):
        # for now just damage event
        events = []
        target = event.target
        damage_amount = event.damage_amount
        knockback = event.knockback
        origin = event.origin
        target.health -= damage_amount
        if target.health <= 0:
            death_event = DeathEvent(target)
            events.append(death_event)
        if knockback:
            # calculate knockback direction here, turn into vector, then send out to give to physics manager. for now, just basic based on direction of entity from target
            # if target.direction_state == DS.LEFT:
            #     kb_vector = [-3, 3]
            # else:
            kb_vector = (1.5, 1)
            momentum_event = AddMomentumEvent(target, kb_vector)
            events.append(momentum_event)
        return events
