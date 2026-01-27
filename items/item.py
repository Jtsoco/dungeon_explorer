from shared_components.rect import Rect
from items.item_registry import ITEM_REGISTRY
from animations.attack_registry import WEAPONS_ANIMATIONS
from animations.shield_registry import SHIELD_ANIMATIONS
from enums.entity_enums import ItemType as IT, WeaponActionState as WAS, WeaponCategory as WC, SHIELD_ACTION_STATE as SAS
class Item():
    def __init__(self, item_type, value, position: list = [0, 0], w_h: tuple = (8, 8), cell_pos=(0,0)):
        self.item_type = item_type  # e.g., "HEALTH", "MANA"
        self.value = value  # e.g., amount of health or mana restored, in case of weapons and shields the specific type
        self.position = position  # (x, y)
        self.w_h = w_h  # (width, height)
        self.rect = Rect(w_h[0], w_h[1], position=position)
        if item_type == IT.WEAPON:
            self.animation_frames = WEAPONS_ANIMATIONS[value][WAS.INVENTORY]

        elif item_type == IT.SHIELD:
            self.animation_frames = SHIELD_ANIMATIONS[value][SAS.INVENTORY]
        else:
            self.animation_frames = ITEM_REGISTRY[item_type]
        self.cell_pos = cell_pos  # (cell_x_min, cell_y_min, cell_x_max, cell_y_max)

        self.current_frame = 0
        self.frame_timer = 0

    def get_current_animation_frame(self):
        # items aren't part of the regular update loop, so they need to manager their frame updates when rendered
        # not the best but eh fine for now, it's not something major
        frame_data = self.animation_frames[self.current_frame]
        self.frame_timer += 1
        if self.frame_timer >= frame_data.duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
        return frame_data
