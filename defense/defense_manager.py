from enums.entity_enums import SHIELD_ACTION_STATE as SAS
from base_manager import BaseManager

from events_commands.commands import DefenseCommand, StartBlockCommand, EndBlockCommand, BreakBlockCommand

class DefenseManager(BaseManager):
    def __init__(self, context=None, local_bus=None):
        super().__init__(context=context)
        self.local_bus = local_bus

    def update(self, entity_data):
        if not entity_data.shield:
            return
        if entity_data.shield.active:
            self.update_shield(entity_data)

    def start_blocking(self, entity_data):
        entity_data.shield.pending_unblock = False
        entity_data.shield.active = True
        entity_data.shield.action_state = SAS.TO_BLOCK
        entity_data.shield.current_frame = 0
        entity_data.shield.frame_timer = 0

    def end_blocking(self, entity_data):
        if entity_data.shield.action_state == SAS.BLOCK:
            self.move_to_rest(entity_data)

        else:
            entity_data.shield.pending_unblock = True

    def move_to_rest(self, entity_data):
        entity_data.shield.action_state = SAS.TO_REST
        entity_data.shield.current_frame = 0
        entity_data.shield.frame_timer = 0
        entity_data.shield.pending_unblock = False

    def break_block(self, entity_data):
        entity_data.shield.pending_unblock = False
        entity_data.shield.action_state = SAS.BROKEN
        entity_data.shield.current_animation = entity_data.shield.animations[SAS.BROKEN]
        entity_data.shield.current_frame = 0
        entity_data.shield.frame_timer = 0
        entity_data.shield.broken_timer = 0

    def update_shield(self, entity_data):
        if self.update_frame_index(entity_data.shield):
            if entity_data.shield.current_frame == 0:
                # finished animaiton, move to next state
                self.next_shield_state(entity_data.shield)
        if entity_data.shields.action_state == SAS.BROKEN:
            # while blocking, reset frame to stay on blocking frame
            entity_data.shield.broken_timer += 1
            if entity_data.shield.broken_timer >= entity_data.shield.broken_recovery_time:
                self.back_to_idle(entity_data)

    def back_to_idle(self, entity_data):
        entity_data.shield.active = False
        entity_data.shield.action_state = SAS.IDLE
        entity_data.shield.current_frame = 0
        entity_data.shield.frame_timer = 0
        entity_data.shield.pending_unblock = False

    def next_shield_frame(self, shield):
        # to black and to rest are the transitory states, otherwise animations repeat
        match shield.action_state:
            case SAS.TO_BLOCK:
                if entity_data.shield.pending_unblock:
                    shield.action_state = SAS.TO_REST
                    entity_data.shield.pending_unblock = False
                else:
                    shield.action_state = SAS.BLOCK
            case SAS.TO_REST:
                shield.action_state = SAS.IDLE
                self.back_to_idle(shield)
                # SEND event that shield is done, so state change occurs, as what a character can do while blocking differs based on shield things, like some allow slow walking some no walking, for default no walking


    def get_current_frame(self, shield):
        return self.get_current_animation(shield)[shield.current_frame]

    def get_current_animation(self, shield):
        return shield.animation[shield.action_state]

    def update_frame_index(self, shield):
        shield.frame_timer += 1
        frame = self.get_current_frame(shield)
        if shield.frame_timer >= frame.duration:
            shield.frame_timer = 0
            shield.current_frame += 1
            self.set_current_frame_index(shield)
            return True
        return False

    def set_current_frame_index(self, shield):
        shield.current_frame %= len(shield.current_animation)

    def handle_command(self, command, entity_data):
        # it only cares about handling what happens to shield, not anything else
        match command:
            case StartBlockCommand():
                self.start_blocking(entity_data)
            case EndBlockCommand():
                self.end_blocking(entity_data)
            case BreakBlockCommand():
                self.break_block(entity_data)
