from base_manager import BaseManager
from events_commands.events import PlayerEvent as PE, PlayerDamagedEvent as PDe, PlayerHealedEvent as PHe, PlayerDeathEvent as PDea
from enums.hud_enums import HUDComponentType as HCT
from HUD.health_component import HealthComponent
from renderers.hud_renderer import HudRenderer


class HUDManager(BaseManager):
    def __init__(self, context):
        super().__init__(context=context)
        self.context = context
        # HUD elements can be initialized here
        # e.g., health bars, score displays, etc.
        self.components = {
            HCT.HEALTH: HealthComponent(max_health=100),
        }
        self.renderer = HudRenderer()

    def get_render_items(self):
        pass

    def setup_bus(self):
        self.context.bus.register_event_listener(PE, self)

    def handle_event(self, event):
        match event:
            case PDe():
                self.handle_damage(event)
            case PHe():
                pass
            case PDea():
                pass

    def handle_damage(self, damage_amount):
        # damage amount isn't needed for now, really just plan to have it as a way to show what degree the health changed by with an animation later
        player = self.context.data_context.player_data
        health_component = self.components[HCT.HEALTH]
        new_health = player.health
        health_component.set_new_health(new_health)

    def handle_updates(self):
        pass

    def draw(self):
        # Draw HUD elements on the screen
        components = list(self.components.values())
        self.renderer.render(components)

    def setup_player_hud(self, player_data):
        health_component = self.components[HCT.HEALTH]

        health_component.set_new_max_health(player_data.health, True)
