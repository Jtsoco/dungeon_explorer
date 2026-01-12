# shield class, holds data
# desired behavior:
# active, deactive
# block stamina drain on every hit
# start animation on block, not truly active until in place
# different shield types have different block properties
# wind down after blocking to unblock
# different block / unblock speeds

# needs to have own animation data for each stage, preblock, blocking, unblock
# is set by entity offhand offset data
# or maybe no offset for now from player, just its offset, and position it like it would be on player otherwise? so long as it fits in player sprite it should be okay, so 8x8
from enums.entity_enums import SHIELD_CATEGORY as SC, SHIELD_ACTION_STATE as SAS
from animations.shield_registry import SHIELD_ANIMATIONS, SHIELD_HITBOXES
class ShieldData:
    def __init__(self, shield_category=SC.IRON_SHIELD, max_stamina=100, drain_resistance=25, animation=SHIELD_ANIMATIONS[SC.IRON_SHIELD], damage_resist=1.0, hitbox=SHIELD_HITBOXES[SC.IRON_SHIELD]):
        self.shield_category = shield_category
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.drain_resistance = drain_resistance  # higher is better, reduces stamina drain
        self.action_state = SAS.IDLE
        self.active = False
        self.damage_resist = damage_resist  # multiplier to reduce damage taken when blocking


        self.animation=animation
        self.hitbox=hitbox
        self.current_frame = 0
        self.frame_timer = 0
        self.broken_recovery__time = 30 # frames to recover from broken state
        self.broken_timer = 0
        self.pending_unblock = False

        self.regen_timer = None
        self.regen_amount = 10
        self.regen_delay = 20
        self.regen_active = False

    def get_current_frame(self):
        return self.animation[self.action_state][self.current_frame]

    def get_current_hitbox(self):
        return self.hitbox

    def get_current_animation(self):
        return self.animation[self.action_state]

    def drain_stamina(self, amount):
        effective_drain = max(0, amount - self.drain_resistance)
        self.current_stamina = max(0, self.current_stamina - effective_drain)
        return effective_drain
