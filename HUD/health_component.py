from enums.hud_enums import HUDComponentType as HE
from HUD.hud_sprite_registry import HUD_REGISTRY
from shared_components.rect import Rect

class HealthComponent():
    def __init__(self, max_health=100):
        self.max_health = max_health
        self.current_health = max_health
        self.sprite_data = HUD_REGISTRY[HE.HEALTH]
        self.sprite_list = []
        self.generate_sprites(current_health=self.current_health)

    def generate_sprites(self, current_health):
        health_demoninators = sorted(self.sprite_data.keys(), reverse=True)
        current_health_remaining = current_health
        sprites = []
        x_offset = 0
        for health_value in health_demoninators:
            while current_health_remaining >= health_value:
                animation_frames = self.sprite_data[health_value]
                heart_sprite = HeartSprite(position=(x_offset, 0), animation_frames=animation_frames)
                sprites.append(heart_sprite)
                current_health_remaining -= health_value
                x_offset += 10

        if current_health_remaining > 0 and (current_health_remaining < health_demoninators[-1]):
            # add smallest heart for remaining health
            animation_frames = self.sprite_data[health_demoninators[-1]]
            heart_sprite = HeartSprite(position=(x_offset, 0), animation_frames=animation_frames)
            sprites.append(heart_sprite)

    def set_new_health(self, new_health):
        self.current_health = max(0, min(new_health, self.max_health))
        hearts = self.generate_sprites(current_health=self.current_health)
        self.sprite_list = hearts

class HeartSprite():
    def __init__(self, position=(0,0), animation_frames=[]):
        self.rect = Rect(w=8, h=8, position=position)
        self.animation_frames = animation_frames
        self.current_frame_index = 0

    def get_current_frame(self):
        return self.animation_frames[self.current_frame_index]
