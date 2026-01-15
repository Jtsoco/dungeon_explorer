from base_manager import BaseManager
from events_commands.events import BossDeathEvent
from enums.entity_enums import PowerUpStates as PUS
from events_commands.commands import TemporaryMessageCommand, SoundCommand
from audio.sound_enums import SoundEnum
class PowerupManager(BaseManager):
    # this class gives powerups to the player and possibly other entities when the time comes
    def __init__(self, context):
        super().__init__(context=context)


    def setup_bus(self):
        self.context.bus.register_event_listener(BossDeathEvent, self)

    def handle_event(self, event):
        pass

    def handle_command(self, command):
        pass

    def notify_event(self, event):
        match event:
            case BossDeathEvent():
                self.grant_boss_powerup(event.entity)

    def grant_boss_powerup(self, entity):
        if entity.powerup_reward:
            # this will set the dictionary to have double jump, as it's enabled by the key existing, and True means can currently use double jump
            self.context.bus.send_command(SoundCommand(sound_enum=SoundEnum.POWER_UP))
            player = self.context.data_context.player_data
            player.power_ups[entity.powerup_reward] = True
            # message differs based on powerup granted
            # but generally for now powerups are like this, just in the powerups key and when trying to use them it'll be checked
            # as things change i'll change how they are granted, but for now as all powerups are like this, this is fine
            match entity.powerup_reward:
                case PUS.DOUBLE_JUMP:
                    message = "Double Jump Acquired!"
                    self.context.bus.send_command(TemporaryMessageCommand(message=message, seconds_duration=3.0))
