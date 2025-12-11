from events_commands.events import InputEvent
from enums.entity_enums import MovementState as MS, InputEnums as IE, DirectionState as DS
import random
from debug.quick_debug import display_info

class SkullController():

    def __init__(self):
        pass
    # a barebones controller for a skull enemy

    def update(self, entity, context=None):
        if context:
            return self.context_update(entity, context)
        else:
            return self.contextless_update(entity)

    def context_update(self, entity, context):
        tile_context = context.tile_context
        events = []
        entity.state_timer += 1

        if entity.movement_state == MS.WALKING:
            if self.check_ledge(entity, context, direction=entity.direction_state) or self.check_edge_of_cell(entity, context, direction=entity.direction_state):
                # reverse direction
                match entity.direction_state:
                    case DS.LEFT:
                        events.append(InputEvent(IE.MOVE, direction=DS.RIGHT))
                    case DS.RIGHT:
                        events.append(InputEvent(IE.MOVE, direction=DS.LEFT))
                entity.state_timer = 0
                return events
        # if no ledge, just do regular contextless update
        events = self.contextless_update(entity)
        return events

    def check_ledge(self, entity, context, direction=DS.LEFT):
        tile_context = context.tile_context
        pos_x = entity.position[0] + entity.w_h[0] if direction == DS.LEFT else entity.position[0]
        return tile_context.at_edge_of_dropoff(pos_x, entity.position[1], entity.w_h[0], entity.w_h[1], direction=direction)
        # false if not at a ledge

    def check_edge_of_cell(self, entity, context, direction=DS.LEFT):
        tile_context = context.tile_context
        return tile_context.at_edge_of_cell_horizontal(entity.cell_pos[0], entity.position[0], entity.w_h[0], direction=direction)
        # false if not at edge of cell, true if so

    def contextless_update(self, entity):
        # with this it may technically be able to fall of a ledge if it starts from idle right in front of it, but eh rework later when i dedicate more time to ai
        selection = [MS.IDLE, MS.WALKING, MS.WALKING]
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
