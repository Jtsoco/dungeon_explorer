from entity.controllers.knight_controller import KnightController
# knight_controller import KnightController
from enums.entity_enums import EntityType as ET, EntityCategory as EC
from events_commands.events import InputEvent
import random

class DarkLordController(KnightController):
    def __init__(self):
        super().__init__()
        self.max_notice_distance = (64, 40)  # x, y distances
        self.action_distance = 30
        self.y_action_distance = 30  # x, y distances
