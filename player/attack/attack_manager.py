from player.player_enums import WeaponActionState as WAS
from events_commands.events import AttackFinishedEvent as AFE
from events_commands.commands import AttackCommand

class AttackManager():
    def __init__(self):
        pass

    def update(self, player_data):
        weapon_data = player_data.weapon_data
        if weapon_data.active:
            self.update_weapon(weapon_data)

    def update_weapon(self, weapon_data):
        if self.update_frame_index(weapon_data):
            if weapon_data.current_frame == 0:
                # finished attack animation
                self.finish_attack(weapon_data)

                return AFE()

    def finish_attack(self, weapon_data):
        weapon_data.active = False
        weapon_data.state = WAS.SHEATHED
        weapon_data.current_animation = weapon_data.animations[WAS.SHEATHED]
        weapon_data.current_frame = 0
        weapon_data.frame_timer = 0
        weapon_data.current_hitbox = None

    def handle_command(self, command, player_data):
        match command:
            case AttackCommand():
                self.start_attack(player_data)
        return [], []  # No new events or commands

    def start_attack(self, player_data):
        # for now, just default. it will decide what attack to set otherwise, but for now there is only one
        weapon_data = player_data.weapon_data
        if not weapon_data.active:
            weapon_data.active = True
            weapon_data.state = WAS.DEFAULT
            weapon_data.current_animation = weapon_data.animations[WAS.DEFAULT]
            weapon_data.current_frame = 0
            weapon_data.frame_timer = 0

    def update_frame_index(self, weapon_data):
        if weapon_data.frame_timer >= weapon_data.current_animation[weapon_data.current_frame].duration:
            weapon_data.current_frame += 1
            weapon_data.frame_timer = 0
            self.set_current_frame_index(weapon_data)
            return True
        return False

    def set_current_frame_index(self, weapon_data):
        weapon_data.current_frame %= len(weapon_data.current_animation)
        # for now this is same as animation manager, but when hitboxes are decoupled (if they are) then this will be different
