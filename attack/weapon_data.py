from enums.entity_enums import AttackType as AT, CollisionEntityTarget as CET, WeaponActionState as WS, WeaponCategory as WC
from audio.sound_enums import SoundEnum
from enums.entity_enums import DirectionState as DS

def default_hitbox():
    dict = {}
    dict[0] = (8, 4)
    dict[1] = (8, 6)
    dict[2] = (8, 8)
    # note, need to add x, y offsets later. for now just width, height
    return dict
from animations.attack_registry import WEAPONS_ANIMATIONS, WEAPONS_HITBOXES


class WeaponData():
    def __init__(self,
                 weapon_type=AT.MELEE,
                 animations=WEAPONS_ANIMATIONS[WC.SHORTSWORD],
                 hitboxes=WEAPONS_HITBOXES[WC.SHORTSWORD],
                 damage=50,
                 target_type=CET.ENEMY,
                 weapon_category=WC.SHORTSWORD,
                 knockback=(1.5, 1), attack_sound=SoundEnum.ATTACK):

        self.state = WS.SHEATHED
        self.active = False
        self.type = weapon_type
        self.category = weapon_category
        self.damage = damage
        self.hitboxes = hitboxes
        self.target_type = target_type
        # self.current_hitbox = None
        # revisit hitbox code later
        # for now the animations are tied to the hitboxes and such, will separate later if desired
        self.animations = animations
        self.attack_sound = attack_sound

        self.current_frame = 0
        self.frame_timer = 0
        self.current_animation = animations[WS.SHEATHED]
        self.current_hitbox = self.hitboxes.get(WS.DEFAULT, default_hitbox())
        # should all have a sheathed animation
        self.knockback = knockback

    def get_current_frame(self):
        return self.current_animation[self.current_frame]
        # when rolled into two separate classes, just use animationData for the animation part. for now, current frame is used across so just using this. Eventually will separate to hitboxes data, animation data, and regular weapon data

    def get_current_hitbox(self):
        if self.active:
            return self.current_hitbox.get(self.current_frame, (0,0))
        # if not active, just give empty hitbox, no collision there
        return (0,0)

    def set_current_hitboxes(self, state=WS.DEFAULT):
        if state in self.hitboxes:
            self.current_hitbox = self.hitboxes[state]
        else:
            self.current_hitbox = default_hitbox()
        # if self.active:
        #     self.current_hitbox = self.hitboxes.get(self.state, {})
        # else:
        #     self.current_hitbox = {}

    def get_position(self, entity_data):
        hitbox = self.get_current_hitbox()
        if entity_data.direction_state == DS.RIGHT:
            attack_x = entity_data.rect.position[0] + entity_data.rect.width
        else:
            attack_x = entity_data.rect.position[0] - hitbox[0]
        attack_y = entity_data.rect.position[1]
        # super simple that doesn't take into account any offsets or anything, revisit later
        return (attack_x, attack_y)
