import pyxel

class HudRenderer():
    def __init__(self):
        pass

    def render(self, hud_components):

        for component in hud_components:
            for sprite in component.sprite_list:
                frame = sprite.get_current_frame()
                position = sprite.rect.position
                # Render the frame at the given position
                # This is a placeholder for actual rendering logic
                pyxel.blt(position[0], position[1], 0, frame.pos[0] * 8, frame.pos[1] * 8, frame.w_h[0], frame.w_h[1], colkey=2)
