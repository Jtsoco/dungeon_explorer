from player.player_enums import WeaponActionState as WAS
from events_commands.events import AttackFinishedEvent as AFE
from events_commands.commands import AttackCommand

class AttackManager():
    def __init__(self):
        pass

    def update(self, player_data):
        if not player_data.weapon:
            return None
        # will create a dummy weapon data later, but also will in general will revisit how this is handled and if i will create a cleaner system that doesn't make calls to things that won't do anything, but for now this is fine
        weapon = player_data.weapon
        if weapon.active:
            return self.update_weapon(weapon)

    def update_weapon(self, weapon):
        if self.update_frame_index(weapon):
            if weapon.current_frame == 0:
                # finished attack animation
                self.finish_attack(weapon)

                return AFE()
        return None

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
            weapon.active = True
            weapon.state = WAS.DEFAULT
            weapon.current_animation = weapon.animations[WAS.DEFAULT]
            weapon.current_frame = 0
            weapon.frame_timer = 0

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
