from entity.controllers.default_controller import DefaultController
from enums.entity_enums import MovementState as MS, DirectionState as DS, InputEnums as IE, SimpleAIState as SAIS
from events_commands.events import InputEvent
import random


class KnightController(DefaultController):
    def __init__(self):
        super().__init__()
        self.long_wait = 90
        self.short_wait = 30
        self.medium_wait = 60
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
        if self.is_target_close(distance):
            new_events = self.player_close(entity, context, distance)
            return new_events
        else:
            if entity.ai != SAIS.PATROL:
                self.back_to_patrol(entity)

        if entity.movement_state == MS.WALKING:
            new_events = self.walking_to_ledge(entity, context)
            if new_events:
                return new_events
        # if no ledge, just do regular contextless update
        events = self.contextless_update(entity)
        return events

    def back_to_patrol(self, entity):
        entity.ai = SAIS.PATROL
        entity.state_timer = 0
        entity.state_timer_limit = random.randint(30, 90)

    def distance_to_player(self, entity, context):
        player_data = context.player_data
        distance_x = abs((entity.position[0] + entity.w_h[0] / 2) - (player_data.position[0] + player_data.w_h[0] / 2))
        distance_y = abs((entity.position[1] + entity.w_h[1] / 2) - (player_data.position[1] + player_data.w_h[1] / 2))
        return (distance_x, distance_y)


    def is_target_close(self, distance):
        distance_x = distance[0]
        distance_y = distance[1]
        if distance_x < 40 and distance_y < 20:
            return True
        return False

    def player_close(self, entity, context, distance):
        player_data = context.player_data
        distance_x = distance[0]
        distance_y = distance[1]
        events = []
        match entity.ai:
            case SAIS.PATROL:
                new_events = self.select_active_action(entity, context, distance_x, distance_y)
                events.extend(new_events)
            case SAIS.CHASE:
                # check if still properly pursuing player in right direction, if not swap directions
                # otherwise reevaluate active action
                if entity.state_timer >= entity.state_timer_limit:
                    new_events = self.select_active_action(entity, context, distance_x, distance_y)
                    events.extend(new_events)
                else:
                    if not self.following_target(entity, player_data):
                        # switch directions
                        events.append(self.swap_directions(entity))
                        entity.state_timer = 0
                        entity.state_timer_limit = self.medium_wait
                    elif distance_x < 10 and distance_y < 10:

                            # in range to attack, so stop moving
                        events.append(InputEvent(IE.STOP_MOVE))
                        # just have it check direction, and if it's too close, stop moving or back up
                    else:
                        if entity.movement_state == MS.IDLE:
                            # move toward player
                            new_events = self.select_active_action(entity, context, distance_x, distance_y)
                            events.extend(new_events)
            case SAIS.ATTACK:
                # just have it check if it's still in range to attack, if not go to chase
                if distance_x > 20 or distance_y > 10:
                    # out of range, go to chase
                    entity.ai = SAIS.CHASE
                    entity.state_timer = 0
                    entity.state_timer_limit = random.randint(self.short_wait, self.long_wait)
                else:
                    # in range, attack again if timer is up
                    if entity.state_timer >= entity.state_timer_limit:
                        events.append(InputEvent(IE.ATTACK))
                        entity.state_timer = 0
                        entity.state_timer_limit = random.randint(self.short_wait, self.long_wait)
            case SAIS.FLEE:
                pass

        return events

    def swap_directions(self, entity):
        match entity.direction_state:
            case DS.LEFT:
                return InputEvent(IE.MOVE, direction=DS.RIGHT)
            case DS.RIGHT:
                return InputEvent(IE.MOVE, direction=DS.LEFT)

    def following_target(self, entity, player_data):
        player_to_left = (entity.position[0] + entity.w_h[0] / 2) >= (player_data.position[0] + player_data.w_h[0] / 2)
        match entity.direction_state:
            case DS.LEFT:
                if player_to_left:
                    return True
            case DS.RIGHT:
                if not player_to_left:
                    return True
        return False

    def select_active_action(self, entity, context, distance_x, distance_y):
        events = []
        player_data = context.player_data
        if distance_x < 20 and distance_y < 10:
            # attack
            events.append(InputEvent(IE.ATTACK))
            entity.state_timer = 0
            entity.state_timer_limit = self.random_wait_time()
            entity.ai = SAIS.ATTACK
            return events
        elif distance_x < 40 and distance_y < 20:
            # move toward player
            if (entity.position[0] + entity.w_h[0] / 2) < (player_data.position[0] + player_data.w_h[0] / 2):
                events.append(InputEvent(IE.MOVE, direction=DS.RIGHT))
            else:
                events.append(InputEvent(IE.MOVE, direction=DS.LEFT))
            entity.ai = SAIS.CHASE
            entity.state_timer = 0
            entity.state_timer_limit = self.short_wait
            return events
        return events

    def random_wait_time(self, short=30, long=90):
        return random.randint(short, long)
