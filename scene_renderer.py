import pyxel

class SceneRenderer():
    def __init__(self, context):
        self.context = context

    def update(self):
        pass

    def draw_one(self, cam_x, cam_y, width, height,):
        # for the most part, cam x and y should match with tile map area coordinates x y to draw
        # print(f"Drawing scene at camera position ({cam_x}, {cam_y}) with size ({width}, {height})")
        pyxel.bltm(cam_x, cam_y, 0, cam_x, cam_y, width, height, colkey=self.context.TRANSPARENT_COLOR)
        # so draw x y of the camera, which will have x y of tile map 0 drawn onto it, of the size of a full cell
        # print(f"Scene drawn at camera position ({cam_x}, {cam_y}) with size ({width}, {height})")
    def draw_multiple(self):
        # will need to compensate for horizontal and vertical possibly
        pass

    def render_effects(self, effects):
        for effect in effects:
            self.render_effect(effect)

    def render_effect(self, effect):
        x = effect.position[0]
        y = effect.position[1]
        current_frame = effect.get_current_animation_frame()
        u = current_frame.pos[0] * 8
        v = current_frame.pos[1] * 8
        width = current_frame.w_h[0]
        height = current_frame.w_h[1]
        rotation = current_frame.rotation
        image_bank = 0
        offset = current_frame.offset
        x += offset[0]
        y += offset[1]
        # just a default because i'm only using this for now
        # default direction doesn't exist in effects for now, might edit later
        print(f"Rendering effect at position ({x}, {y}) with frame u:{u}, v:{v}, width:{width}, height:{height}")
        pyxel.blt(x, y, image_bank, u, v, width, height, self.context.TRANSPARENT_COLOR, rotate=rotation)
