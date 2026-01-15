from base_manager import BaseManager
from events_commands.events import BossDeathEvent, DeathEvent, PlayerHealedEvent
from events_commands.commands import HandleItemCommand
from enums.entity_enums import ItemType as IT, ItemAction as IA
import random
from items.item import Item
from events_commands.commands import LoadItemCommand, SoundCommand

from enums.hud_enums import HUDComponentType
from audio.sound_enums import SoundEnum



class ItemManager(BaseManager):
    # this class manages items in the game world, including spawning, despawning, and player interactions
    def __init__(self, context):
        super().__init__(context=context)

    def setup_bus(self):
        self.context.bus.register_event_listener(BossDeathEvent, self)
        self.context.bus.register_event_listener(DeathEvent, self)
        self.context.bus.register_command_listener(HandleItemCommand, self)

    def notify_event(self, event):
        match event:
            case DeathEvent():
                self.handle_death_event(event)

    def notify_command(self, command):
        match command:
            case HandleItemCommand():
                self.handle_item_interaction(command)

    def handle_death_event(self, event):
        chance = random.randint(1, 10)
        if chance <= 3:
            self.spawn_item_at_entity(event.entity)

    def spawn_item_at_entity(self, entity):
        # for now just health
        item_type = IT.HEALTH
        value = 25 * random.randint(1, 3)
        position = entity.rect.position.copy()
        item_w_h = (8, 8)
        item = Item(item_type=item_type, value=value, position=position, w_h=item_w_h, cell_pos=entity.cell_pos)
        self.context.bus.send_command(LoadItemCommand(item=item))

    def handle_command(self, command):
        match command:
            case HandleItemCommand():
                self.handle_item_interaction(command)



    def handle_item_interaction(self, command):
        item_entity = command.item_entity
        action = command.action
        match action:
            case IA.PICKUP:
                self.pickup_item(item_entity)
                # honestly might not include drop
            # case IA.DROP:
            #     self.drop_item(item_entity)

    def pickup_item(self, item_entity):
        # Logic for picking up the item
        match item_entity.item_type:
            case IT.HEALTH:
                player = self.context.data_context.player_data
                player.health = min(player.max_health, player.health + item_entity.value)
                player_healed_event = PlayerHealedEvent(heal_amount=item_entity.value)
                self.context.bus.send_event(player_healed_event)
        self.context.bus.send_command(LoadItemCommand(item=item_entity, load=False))
        self.context.bus.send_command(SoundCommand(sound_enum=SoundEnum.ITEM_GET))
            # case IT.MANA:
            #     player = self.context.data_context.player_data
            #     player.mana = min(player.max_mana, player.mana + item_entity.value)

    def drop_item(self, item_entity):
        # Logic for dropping the item
        pass
