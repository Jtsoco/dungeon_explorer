from entity.controllers.default_controller import DefaultController
from enums.entity_enums import MovementState as MS, DirectionState as DS, InputEnums as IE, SimpleAIState as SAIS
from entity.controllers.knight_controller import KnightController
from events_commands.events import InputEvent
import random

class WingedKnightController(KnightController):
    def __init__(self):
        super().__init__()
        self.long_wait = 90
        self.short_wait = 30
        self.medium_wait = 60
        self.max_notice_distance = (70, 30)  # x, y distances
        # for now, just inherit default controller behavior


    def jump(self, entity):
        # simple jump command for AI
        if entity.movement_state != MS.JUMPING:
            return InputEvent(IE.JUMP)
        elif entity.movement_state == MS.JUMPING and self.max_arc_height_reached(entity):
            return InputEvent(IE.JUMP)
        return None

    def max_arc_height_reached(self, entity):
        movement_state = entity.movement_state
        velocity_y = entity.velocity[1]
        if velocity_y >= -1 and velocity_y <= 1 and (movement_state == MS.JUMPING or movement_state == MS.FALLING):
            # see if at apex of jump/fall
            return True
        # close enough to zero
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
                    elif entity.movement_state == MS.IDLE:
                            # move toward player
                            new_events = self.select_active_action(entity, context, distance_x, distance_y)
                            events.extend(new_events)
            case SAIS.JUMP_ATTACK:
                if entity.state_timer >= entity.state_timer_limit:
                    new_events = self.select_active_action(entity, context, distance_x, distance_y)
                    events.extend(new_events)
                elif self.max_arc_height_reached(entity):
                    # figure out if they will attempt a second jump, or just attack again in the air
                    event = self.ariel_maneuver()
                    if event.input_type == IE.JUMP:
                        entity.state_timer = 0
                        entity.state_timer_limit = self.long_wait
                        # continue jump attack
                        # momentum should change, and ariel momentum shouldn't trigger again, unless its max height of double jump, then velocity won't chnage so it should be max height again and trigger ariel maneuver again
                    else:
                        entity.ai = SAIS.ATTACK
                        # jump attack should techincally be over here
                        entity.state_timer = 0
                        entity.state_timer_limit = random.randint(self.short_wait, self.long_wait)
                    events.append(event)
                elif entity.movement_state != MS.JUMPING and entity.movement_state != MS.FALLING:
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


    def select_active_action(self, entity, context, distance_x, distance_y):
        events = []
        player_data = context.player_data
        if distance_x < 10 and distance_y < 10:
            # attack
            events.append(InputEvent(IE.ATTACK))
            entity.state_timer = 0
            entity.state_timer_limit = self.random_wait_time()
            entity.ai = SAIS.ATTACK
        elif distance_x < 20 and distance_y < 15:
            # move toward player
            events = self.set_chase(entity, player_data)
        else:
            new_events = self.set_chase(entity, player_data)
            new_events.extend(self.jump_attack(entity))
            events.extend(new_events)
        return events

    def set_chase(self, entity, player_data):
        events = []
        if (entity.position[0] + entity.w_h[0] / 2) < (player_data.position[0] + player_data.w_h[0] / 2):
                events.append(InputEvent(IE.MOVE, direction=DS.RIGHT))
        else:
            events.append(InputEvent(IE.MOVE, direction=DS.LEFT))
        entity.ai = SAIS.CHASE
        entity.state_timer = 0
        entity.state_timer_limit = self.short_wait
        return events

    def jump_attack(self, entity):
        events = []
        jump_event = self.jump(entity)
        if jump_event:
            events.append(jump_event)
        # events.append(InputEvent(IE.ATTACK))
        entity.ai = SAIS.JUMP_ATTACK
        entity.state_timer = 0
        entity.state_timer_limit = self.long_wait
        # TODO think about whether to have separate attack, and movement ai states or not. For now this is fine, but when it comes time for more robust things revisit this
        return events

    def ariel_maneuver(self):
        # decide whether to do another jump or just attack again in air
        choice = random.choice([IE.ATTACK, IE.JUMP])
        return InputEvent(choice)
