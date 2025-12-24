from entity.controllers.default_controller import DefaultController
from enums.entity_enums import MovementState as MS, DirectionState as DS, InputEnums as IE
from events_commands.events import InputEvent


class KnightController(DefaultController):
    def __init__(self):
        super().__init__()
        # for now, just inherit default controller behavior

    def contextless_update(self, entity):
        return super().contextless_update(entity)

    def update(self, entity, context=None):
        entity.state_timer += 1
        if context:
            return self.context_update(entity, context)
        else:
            return self.contextless_update(entity)

    def context_update(self, entity, context):
        tile_context = context.tile_context
        events = []
        distance = self.distance_to_player(entity, context)
        if self.player_close(entity, context, distance):
            new_events = self.player_close(entity, context, distance)
            return new_events
        if entity.movement_state == MS.WALKING:
            new_events = self.walking_to_ledge(entity, context)
            if new_events:
                return new_events
        # if no ledge, just do regular contextless update
        events = self.contextless_update(entity)
        return events

    def distance_to_player(self, entity, context):
        player_data = context.player_data
        distance_x = abs((entity.position[0] + entity.w_h[0] / 2) - (player_data.position[0] + player_data.w_h[0] / 2))
        distance_y = abs((entity.position[1] + entity.w_h[1] / 2) - (player_data.position[1] + player_data.w_h[1] / 2))
        return (distance_x, distance_y)

    def player_close(self, entity, context, distance_to_player):

        if distance_to_player[0] < 40 and distance_to_player[1] < 20:
            return True
        return False

    def player_close(self, entity, context, distance):
        player_data = context.player_data
        distance_x = distance[0]
        distance_y = distance[1]
        events = []
        if distance_x < 20 and distance_y < 10:
            # attack
            events.append(InputEvent(IE.ATTACK))
            entity.state_timer = 0
            entity.state_timer_limit = 30
            return events
        elif distance_x < 40 and distance_y < 20:
            # move toward player
            if (entity.position[0] + entity.w_h[0] / 2) < (player_data.position[0] + player_data.w_h[0] / 2):
                events.append(InputEvent(IE.MOVE, direction=DS.RIGHT))
            else:
                events.append(InputEvent(IE.MOVE, direction=DS.LEFT))
            entity.state_timer = 0
            entity.state_timer_limit = 30
            return events
        return None
