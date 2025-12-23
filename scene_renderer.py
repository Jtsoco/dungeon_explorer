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
