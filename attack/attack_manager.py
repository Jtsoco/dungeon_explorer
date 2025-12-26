from enums.entity_enums import WeaponActionState as WAS, MovementState as MS, CollisionEntityTarget as CET, DirectionState as DS
from events_commands.events import AttackFinishedEvent as AFE, PossibleAttackCollisionEvent as PACE
from events_commands.commands import AttackCommand


class AttackManager():
    def __init__(self):
        pass

    def update(self, player_data):
        if not player_data.weapon:
            return None
        # will create a dummy weapon data later, but also will in general will revisit how this is handled and if i will create a cleaner system that doesn't make calls to things that won't do anything, but for now this is fine
        if player_data.weapon.active:
            return self.update_weapon(player_data)

    def update_weapon(self, entity_data):
        if self.update_frame_index(entity_data.weapon):
            if entity_data.weapon.current_frame == 0:
                # finished attack animation
                self.finish_attack(entity_data.weapon)

                return AFE()
        pos = self.get_position(entity_data)
        return PACE(entity_data, attack_position=pos, target_type=entity_data.weapon.target_type)


    def get_position(self, entity_data):
        weapon = entity_data.weapon
        hitbox = weapon.get_current_hitbox()
        if entity_data.direction_state == DS.RIGHT:
            attack_x = entity_data.position[0] + entity_data.w_h[0]
        else:
            attack_x = entity_data.position[0] - hitbox[0]
        attack_y = entity_data.position[1]
        # super simple that doesn't take into account any offsets or anything, revisit later
        return (attack_x, attack_y)

    def finish_attack(self, weapon):
        weapon.active = False
        weapon.state = WAS.SHEATHED
        weapon.current_animation = weapon.animations[WAS.SHEATHED]
        weapon.current_frame = 0
        weapon.frame_timer = 0
        weapon.current_hitbox = None

    def handle_command(self, command, player_data):
        match command:
            case AttackCommand():
                self.start_attack(player_data)
        return [], []  # No new events or commands

    def start_attack(self, player_data):
        # for now, just default. it will decide what attack to set otherwise, but for now there is only one
        weapon = player_data.weapon
        if not weapon.active:
            player_state = player_data.movement_state
            weapon.active = True
            match player_state:
                case MS.FALLING | MS.JUMPING:
                    state = self.get_jump_attack(weapon)
                case _:
                    state = WAS.DEFAULT
            weapon.current_animation = weapon.animations[state]
            weapon.state = state
            weapon.current_frame = 0
            weapon.frame_timer = 0

    def get_jump_attack(self, weapon_data):
        if WAS.AIRATTACK in weapon_data.animations:
            return WAS.AIRATTACK
        return WAS.DEFAULT

    def update_frame_index(self, weapon):
        if weapon.frame_timer >= weapon.current_animation[weapon.current_frame].duration:
            weapon.current_frame += 1
            weapon.frame_timer = 0
            self.set_current_frame_index(weapon)
            return True
        weapon.frame_timer += 1
        return False

    def set_current_frame_index(self, weapon):
        weapon.current_frame %= len(weapon.current_animation)
        # for now this is same as animation manager, but when hitboxes are decoupled (if they are) then this will be different
