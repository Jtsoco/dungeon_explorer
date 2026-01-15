from base_manager import BaseManager
from events_commands.events import PlayerEvent as PE, PlayerDamagedEvent as PDe, PlayerHealedEvent as PHe, PlayerDeathEvent as PDea, PlayerShieldDamagedEvent as PSDe
from events_commands.commands import HUDCommand, TemporaryMessageCommand
from enums.hud_enums import HUDComponentType as HCT
from renderers.hud_renderer import HudRenderer
from HUD.temporary_message import TemporaryMessage
from magic_numbers import FPS
from HUD.sprite_component import SpriteComponent


class HUDManager(BaseManager):
    def __init__(self, context):
        super().__init__(context=context)
        self.context = context
        # HUD elements can be initialized here
        # e.g., health bars, score displays, etc.
        self.components = {
            HCT.HEALTH: SpriteComponent(max_value=100),
            HCT.SHIELD: SpriteComponent(max_value=100, x_offset=-10, start_position=(0, 10), sprite_enum=HCT.SHIELD),
        }
        self.renderer = HudRenderer()
        self.temporary_messages = []  # For displaying temporary messages on HUD

    def get_render_items(self):
        pass

    def setup_bus(self):
        self.context.bus.register_event_listener(PE, self)
        self.context.bus.register_command_listener(HUDCommand, self)

    def handle_event(self, event):
        match event:
            case PDe():
                self.handle_damage(event)
            case PHe():
                self.handle_damage(event)
            case PDea():
                pass
            case PSDe():
                self.handle_damage(event, HCT.SHIELD)

    def handle_command(self, command):
        match command:
            case TemporaryMessageCommand():
                self.make_temporary_message(command.message, command.seconds_duration)

    def make_temporary_message(self, message, seconds_duration):
        # for now fps is hardlocked to 30, will eventuall change it so context provides it but for now, let it be a constant
        fps = FPS
        total_frames = int(seconds_duration * fps)
        temp_message = TemporaryMessage(message, total_frames)
        self.temporary_messages.append(temp_message)

    def handle_damage(self, event, component_type=HCT.HEALTH):
        # damage amount isn't needed for now, really just plan to have it as a way to show what degree the health changed by with an animation later
        player = self.context.data_context.player_data
        component = self.components[component_type]
        match component_type:
            case HCT.HEALTH:
                new_value = player.health
            case HCT.SHIELD:
                new_value = player.shield.current_stamina
        component.set_new_value(new_value)

    def handle_updates(self):
        # for now, just have temporary commmands play one at a time, when one is done
        if self.temporary_messages:
            # update the first message, it returns true if it's done
            if self.temporary_messages[0].update():
                self.temporary_messages.pop(0)


    def draw(self):
        # Draw HUD elements on the screen
        components = list(self.components.values())
        self.renderer.render(components)

        if self.temporary_messages:
            # draw the first message
            message = self.temporary_messages[0]
            self.renderer.render_message(message.message)
        # self.renderer.render_message('Test Message, how easy to read?')

    def setup_player_hud(self, player_data):
        health_component = self.components[HCT.HEALTH]

        health_component.set_new_max_value(player_data.health, True)

        shield_component = self.components[HCT.SHIELD]
        shield_component.set_new_max_value(player_data.shield.max_stamina, True)
