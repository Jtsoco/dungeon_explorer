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

    def render_message(self, message, position=(10, 10), color=7):
        for i in range(-1, 2, 2):
            # make a shadow effect for readability
            pyxel.text(position[0]+i, position[1], message, 0)
            pyxel.text(position[0], position[1]+i, message, 0)
            pyxel.text(position[0]+i, position[1]+i, message, 0)
            pyxel.text(position[0]+i, position[1]-i, message, 0)
        pyxel.text(position[0], position[1], message, color)
