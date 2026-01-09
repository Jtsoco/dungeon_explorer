from base_manager import BaseManager
from events_commands.events import BossDeathEvent
from enums.entity_enums import PowerUpStates as PUS

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
            match entity.powerup_reward:
                case PUS.DOUBLE_JUMP:
                    # this will set the dictionary to have double jump, as it's enabled by the key existing, and True means can currently use double jump
                    player = self.context.data_context.player_data
                    player.power_ups[PUS.DOUBLE_JUMP] = True
                    print("Player granted double jump powerup!")
                    # next send notifaction to HUD to show player got double jump
