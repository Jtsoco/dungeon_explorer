from entity.controllers.knight_controller import KnightController
# knight_controller import KnightController
from enums.entity_enums import EntityType as ET, EntityCategory as EC, MovementState as MS, DirectionState as DS, InputEnums as IE, SimpleAIState as SAIS
from events_commands.events import InputEvent, MusicInputEvent
import random

class DarkLordController(KnightController):
    def __init__(self):
        super().__init__()
        self.max_notice_distance = (64, 40)  # x, y distances
        self.action_distance = 30
        self.y_action_distance = 30  # x, y distances
        self.first_encounter = False

    def player_close(self, entity, context, distance):
        player_data = context.data_context.player_data
        distance_x = distance[0]
        distance_y = distance[1]
        events = []
        match entity.ai:
            case SAIS.PATROL:
                new_events = self.select_active_action(entity, context, distance_x, distance_y)
                events.extend(new_events)
                if not self.first_encounter:
                    self.first_encounter = True
                    events.append(MusicInputEvent(IE.MUSIC, music_enum=2))
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
                if distance_x > self.action_distance or distance_y > 10:
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
