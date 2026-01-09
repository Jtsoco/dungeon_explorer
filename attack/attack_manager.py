from enums.entity_enums import WeaponActionState as WAS, MovementState as MS, CollisionEntityTarget as CET, DirectionState as DS
from events_commands.events import AttackFinishedEvent as AFE, PossibleAttackCollisionEvent as PACE
from events_commands.commands import AttackCommand, SoundCommand, LoadActiveAttackCollisionCommand as LAACC
from audio.sound_enums import SoundEnum
from base_manager import BaseManager

class AttackManager(BaseManager):
    def __init__(self, context, local_bus):
        super().__init__(context=context)
        self.context = context
        self.local_bus = local_bus

    def update(self, entity_data):
        if not entity_data.weapon:
            return None
        # will create a dummy weapon data later, but also will in general will revisit how this is handled and if i will create a cleaner system that doesn't make calls to things that won't do anything, but for now this is fine
        if entity_data.weapon.active:
            self.update_weapon(entity_data)

    def update_weapon(self, entity_data):
        if self.update_frame_index(entity_data.weapon):
            if entity_data.weapon.current_frame == 0:
                # finished attack animation
                self.finish_attack(entity_data.weapon)
                self.context.bus.send_command(LAACC(load=False, attacking_entity=entity_data))
                self.local_bus.send_event(AFE())
        # pos = self.get_position(entity_data)
        # return PACE(entity_data, attack_position=pos, target_type=entity_data.weapon.target_type)



    def get_position(self, entity_data):
        # TODO delete possibly, collision might retrieve position instead
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
        weapon.set_current_hitboxes(WAS.SHEATHED)

    def handle_command(self, command, entity_data):
        match command:
            case AttackCommand():
                self.start_attack(entity_data)

    def start_attack(self, entity_data):
        # for now, just default. it will decide what attack to set otherwise, but for now there is only one
        weapon = entity_data.weapon
        if not weapon.active:
            player_state = entity_data.movement_state
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
            weapon.set_current_hitboxes(state)
            self.context.bus.send_command(SoundCommand(sound_enum=weapon.attack_sound))
            self.context.bus.send_command(LAACC(load=True, attacking_entity=entity_data))


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
