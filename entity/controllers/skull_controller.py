from events_commands.events import InputEvent
from enums.entity_enums import MovementState as MS, InputEnums as IE, DirectionState as DS
import random

class SkullController():

    def __init__(self):
        pass
    # a barebones controller for a skull enemy

    def update(self, entity):
        selection = [MS.WALKING, MS.WALKING]
        events = []
        time = entity.state_timer
        entity.state_timer += 1
        if time >= 60:
            # get random from selection
            choice = random.choice(selection)
            match choice:
                case MS.IDLE:
                    events.append(InputEvent(IE.STOP_MOVE))
                case MS.WALKING:
                    direction = random.choice([DS.LEFT, DS.RIGHT])
                    events.append(InputEvent(IE.MOVE, direction=direction))
            entity.state_timer = 0

        return events

    # def update(self, entity, context):
    #     # override for entity update
    #     # context lets it have the intelligence to notice if it's about to fall off a ledge
    #     pass
