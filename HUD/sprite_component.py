from enums.hud_enums import HUDComponentType as HE
from HUD.hud_sprite_registry import HUD_REGISTRY
from shared_components.rect import Rect

class SpriteComponent():
    # this is a generic sprite component for HUD elements
    # things like health and defense which use multiple sprites to display things will use this

    def __init__(self, max_value=1000, current_value=100, sprite_enum=HE.HEALTH, start_position=(0,0), x_offset=10, y_offset=0):
        self.max_value = max_value
        self.current_value = current_value
        self.sprite_data = HUD_REGISTRY[sprite_enum]
        self.start_position = start_position
        self.x_offset = x_offset
        self.y_offset = y_offset

    def generate_sprites(self, current_value):
        value_denominators = sorted(self.sprite_data.keys(), reverse=True)
        current_value_remaining = current_value
        sprites = []
        x_offset = 0
        y_offset = 0
        for value in value_denominators:
            while current_value_remaining >= value:
                animation_frames = self.sprite_data[value]
                hud_sprite = HUDSprite(position=(self.start_position[0]+ x_offset, self.start_position[1]+y_offset), animation_frames=animation_frames)
                sprites.append(hud_sprite)
                current_value_remaining -= value
                x_offset += self.x_offset
                y_offset += self.y_offset
        if current_value_remaining > 0 and (current_value < value_denominators[-1]):
            # add smallest sprite for remaining value
            animation_frames = self.sprite_data[value_denominators[-1]]
            hud_sprite = HUDSprite(position=(self.start_position[0]+ x_offset, self.start_position[1]+y_offset), animation_frames=animation_frames)
            sprites.append(hud_sprite)
        return sprites

    def set_new_value(self, new_value):
        self.current_value = max(0, min(new_value, self.max_value))
        sprites = self.generate_sprites(current_value=self.current_value)
        self.sprite_list = sprites

    def set_new_max_value(self, new_max_value, reset_value=False):
        # self.max_value = new_max_value
        # if reset_value:
        #     self.current_value = new_max_value
        # for now, as it's just hud, don't allow new setting of max value

        self.set_new_value(self.current_value)

class HUDSprite():
    def __init__(self, position=(0,0), animation_frames=[]):
        self.rect = Rect(w=8, h=8, position=position)
        self.animation_frames = animation_frames
        self.current_frame_index = 0

    def get_current_frame(self):
        return self.animation_frames[self.current_frame_index]
