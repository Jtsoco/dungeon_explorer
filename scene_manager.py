from map_camera import MapCamera
from scene_renderer import SceneRenderer
from base_manager import BaseManager
class SceneManager(BaseManager):
    def __init__(self, context):
        super().__init__(context=context)
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
        width = self.context.data_context.CELL_SIZE * self.context.data_context.BRICK_SIZE
        height = self.context.data_context.CELL_SIZE * self.context.data_context.BRICK_SIZE
        self.renderer.draw_one(cam_x, cam_y, width, height)

    def render_effects(self, effects):
        self.renderer.render_effects(effects)

    def render_items(self, items):
        self.renderer.render_items(items)

    def notify(self, event):
        # event will be a custom event class later
        pass

    def set_camera_to_current(self):
        self.camera.set_camera_to_current()

    def set_camera_to_zero(self):
        self.camera.set_absolute_position(0, 0)
