from base_manager import BaseManager
from events_commands.events import PlayerEvent as PE, PlayerDamagedEvent as PDe, PlayerHealedEvent as PHe, PlayerDeathEvent as PDea


class HUDManager(BaseManager):
    def __init__(self, context):
        super().__init__(context=context)
        self.context = context
        # HUD elements can be initialized here
        # e.g., health bars, score displays, etc.


    def get_render_items(self):
        pass

    def setup_bus(self):
        self.context.bus.register_event_listener(PE, self)

    def handle_event(self, event):
        match event:
            case PDe(damage_amount):
                pass
            case PHe(heal_amount):
                pass
            case PDea():
                pass

    def handle_updates(self):
        pass

    def draw(self):
        # Draw HUD elements on the screen
        pass
