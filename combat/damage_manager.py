from enums.entity_enums import DirectionState as DS
from events_commands.events import DeathEvent, PlayerDamagedEvent, BossDeathEvent
from events_commands.commands import SoundCommand, DamageCommand, AddMomentumCommand, CombatCommand, ShieldHitCommand, EntitySeparationCommand
from audio.sound_enums import SoundEnum
from base_manager import BaseManager
class DamageManager(BaseManager):
    def __init__(self, context):
        super().__init__(context)


    # goal of this class as of now:
    # receive damage events, apply damage to entities, handle sending out any resulting events like death events

    def setup_bus(self):
        self.context.bus.register_command_listener(CombatCommand, self)

    def handle_command(self, command):
        events, commands = [], []
        match command:
            case DamageCommand():
                # todo make damage command send them by itself, not return
                events, commands = self.handle_damage(command)
            case ShieldHitCommand():
                self.handle_shield_hit(command)
        for event in events:
            self.context.bus.send_event(event)
        for command in commands:
            self.context.bus.send_command(command)


    def handle_shield_hit(self, shield_hit):
        # for now just damage shield, and use entity separation event to push back attacker
        events = []
        commands = []
        target = shield_hit.target
        damage_amount = shield_hit.damage_amount
        knockback = shield_hit.knockback
        origin = shield_hit.origin
        # if no knockback to shield user, then use this to just separate them
        self.context.bus.send_command(EntitySeparationCommand(origin, target, b_only=True))

    def handle_damage(self, damage):
        # for now just damage damage
        events = []
        commands = []

        target = damage.target
        damage_amount = damage.damage_amount
        knockback = damage.knockback
        origin = damage.origin

        target.health -= damage_amount
        if target.player:
            player_damaged_event = PlayerDamagedEvent(damage_amount)
            events.append(player_damaged_event)
            events.append(player_damaged_event)

        if target.health <= 0:
            if target.boss:
                boss_death_event = BossDeathEvent(target)
                events.append(boss_death_event)

            death_event = DeathEvent(target)
            events.append(death_event)
            commands.append(SoundCommand(sound_enum=SoundEnum.DEATH))  # DEATH sound
        else:
            commands.append(SoundCommand(sound_enum=SoundEnum.DAMAGE))  # HIT sound
        if knockback != (0, 0):
            # calculate knockback direction here, turn into vector, then send out to give to physics manager. for now, just basic based on direction of entity from target
            # if target.direction_state == DS.LEFT:
            #     kb_vector = [-3, 3]
            # else:
            if determine_relative_direction(origin, target) == DS.LEFT:
                kb_vector = [-knockback[0], knockback[1]]
            else:
                kb_vector = [knockback[0], knockback[1]]
            momentum_event = AddMomentumCommand(target, kb_vector)
            commands.append(momentum_event)

        return events, commands

def determine_relative_direction(origin, target):
    # simple implementation for now
    # eventually I plan to use a single knockback value, and determine direction based on relative positions, but for now just this
    if origin.rect.position[0] < target.rect.position[0]:
        return DS.RIGHT
    else:
        return DS.LEFT
