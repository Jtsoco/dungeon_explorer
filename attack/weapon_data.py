from enums.entity_enums import AttackType as AT, CollisionEntityTarget as CET, WeaponActionState as WS


def default_hitbox():
    dict = {}
    dict[0] = (8, 4)
    dict[1] = (8, 6)
    dict[2] = (8, 8)
    # note, need to add x, y offsets later. for now just width, height
    return dict
from animations.animation_setup import default_attack_animation



class WeaponData():
    def __init__(self, animations=default_attack_animation(), weapon_type=AT.MELEE, damage=50, hitboxes=default_hitbox(), target_type=CET.ENEMY, knockback=(1.5, 1)):
        self.state = WS.SHEATHED
        self.active = False
        self.type = weapon_type
        self.damage = damage
        self.hitboxes = hitboxes
        self.target_type = target_type
        # self.current_hitbox = None
        # revisit hitbox code later
        # for now the animations are tied to the hitboxes and such, will separate later if desired
        self.animations = animations

        self.current_frame = 0
        self.frame_timer = 0
        self.current_animation = animations[WS.SHEATHED]
        # should all have a sheathed animation
        self.knockback = knockback

    def get_current_frame(self):
        return self.current_animation[self.current_frame]
        # when rolled into two separate classes, just use animationData for the animation part. for now, current frame is used across so just using this. Eventually will separate to hitboxes data, animation data, and regular weapon data

    def get_current_hitbox(self):
        if self.active:
            return self.hitboxes.get(self.current_frame, (0,0))
        # if not active, just give empty hitbox, no collision there
        return (0,0)
