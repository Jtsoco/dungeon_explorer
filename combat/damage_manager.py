from enums.entity_enums import DirectionState as DS
from events_commands.events import DeathEvent, AddMomentumEvent
from events_commands.commands import SoundCommand
from audio.sound_enums import SoundEnum
from base_manager import BaseManager
class DamageManager(BaseManager):
    def __init__(self, context):
        super().__init__(context)
        pass

    # goal of this class as of now:
    # receive damage events, apply damage to entities, handle sending out any resulting events like death events

    def handle_event(self, event):
        # for now just damage event
        events = []
        commands = []

        target = event.target
        damage_amount = event.damage_amount
        knockback = event.knockback
        origin = event.origin

        target.health -= damage_amount
        if target.health <= 0:
            death_event = DeathEvent(target)
            events.append(death_event)
            commands.append(SoundCommand(sound_enum=SoundEnum.DEATH))  # DEATH sound
        else:
            commands.append(SoundCommand(sound_enum=SoundEnum.DAMAGE))  # HIT sound
        if knockback != (0, 0):
            # calculate knockback direction here, turn into vector, then send out to give to physics manager. for now, just basic based on direction of entity from target
            # if target.direction_state == DS.LEFT:
            #     kb_vector = [-3, 3]
            # else:
            if determine_relative_direction(origin, target) == DS.LEFT:
                kb_vector = [-knockback[0], knockback[1]]
            else:
                kb_vector = [knockback[0], knockback[1]]
            momentum_event = AddMomentumEvent(target, kb_vector)
            events.append(momentum_event)

        return events, commands

def determine_relative_direction(origin, target):
    # simple implementation for now
    # eventually I plan to use a single knockback value, and determine direction based on relative positions, but for now just this
    if origin.position[0] < target.position[0]:
        return DS.RIGHT
    else:
        return DS.LEFT
