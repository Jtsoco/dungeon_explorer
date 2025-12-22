from map_camera import MapCamera
from scene_renderer import SceneRenderer

class SceneManager():
    def __init__(self, context):
        # notifies camera when an event related to cell transition occurs
        self.context = context
        self.camera = MapCamera(context)
        self.renderer = SceneRenderer(context)

    def update(self):
        # possibly make an update queu camera can add and remove itself from later based on scene transitions, for now just always update
        # will need to draw the entirety of the active cells during transitions
        # so will need to grab from camera class size of active space to draw
        pass

    def draw(self):
        # for now, just a single cell draw with no transitions, so keep it simple as of now
        cam_x, cam_y = self.camera.space_to_draw()
        width = self.context.CELL_SIZE * self.context.BRICK_SIZE
        height = self.context.CELL_SIZE * self.context.BRICK_SIZE
        self.renderer.draw_one(cam_x, cam_y, width, height)

    def notify(self, event):
        # event will be a custom event class later
        pass

class Effect:
    # a class for scene effects, like little animations for deaths and such
    def __init__(self, effect_type, position, animation_frames):
        self.effect_type = effect_type
        self.position = position
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.finished = False

    def update(self):
        pass
    # base on animation_manager methods, probably consolidate things into a module later
