import pyxel

class MapCamera():
    # create a renderer class to handle the drawing of cells, using info from camera which handles transitions and positioning

    def __init__(self, context, target=None):
        self.context = context
        self.state = 'idle'
        # change later to proper state machine, but possible just leave it as enums depending on how complex. So far, just idle and transitioning will be needed
        # actually probably will use a state class, with the states keeping track of necessary data for transitions
        self.current_camera = (0, 0)
        self.current_size = (context.data_context.CELL_SIZE * context.data_context.BRICK_SIZE, context.data_context.CELL_SIZE * context.data_context.BRICK_SIZE)
        self.set_camera_cell(context.data_context.start_cell)
        self._target = target
        # target must have a position attribute known as position
        # this will be the center of the camera
        self.disp_x = (context.data_context.CELL_SIZE / 2) * context.data_context.BRICK_SIZE
        self.disp_y = (context.data_context.CELL_SIZE / 2) * context.data_context.BRICK_SIZE

    # set camera will be state specific when further implemented

    def set_camera_cell(self, cell_coordinates: tuple):
        camera_x = cell_coordinates[0] * self.context.data_context.CELL_SIZE * self.context.data_context.BRICK_SIZE
        camera_y = cell_coordinates[1] * self.context.data_context.CELL_SIZE * self.context.data_context.BRICK_SIZE
        pyxel.camera(camera_x, camera_y)
        self.current_camera = (camera_x, camera_y)
        self.current_size = (self.context.data_context.CELL_SIZE * self.context.data_context.BRICK_SIZE, self.context.data_context.CELL_SIZE * self.context.data_context.BRICK_SIZE)



    def set_absolute_position(self, x: int, y: int):
        pyxel.camera(x, y)

    def set_target(self, target):
        self._target = target

    def get_target_point(self):
        if self._target:
            return self._target.position
        return None

    def update(self):
        tx, ty = self.get_target_point()
        centered_x = tx - self.disp_x
        centered_y = ty - self.disp_y
        self.set_absolute_position(centered_x, centered_y)
        self.current_camera = (centered_x, centered_y)
        # no displacement for now, nor events just this


    def space_to_draw(self):
        # if one cell, only active cell. if two, two cells total space
        return self.current_camera


    # needs to handle drawing a cell (active cell based on context.data_context)
    # or if its in a transition, to handle the cell transition by entering a transition state showing half of each cell that's active
    # transitioning in when an event comes marking cell transition
    # leaving when the cell transition is over
    # but also handling a gradual transition to the new camera position

    # so needs two states: normal cell and transitioning, where transitioning


    # Should he just walk between cells, doing it metroid style where the whole screen rolls when edge is hit? or should it be the case where once the edge is hit the camera starts transitioning with the player?
    # if the latter, a quick smooth transition to follow the player as the center of the screen, then once out of cell transition zone it goes to focus on the cell again
    # so in that case three states: follow player x, follow player y, focus on cell
    # done right it would be easy to switch to a full follow the player style camera
    # could be useful to use different camera mini classesfor differnt styles, follow x follow y focus cell follow full

    # also an idea, make a special tile to mark beginning and end of transition zones for full camera, and check edge of screen if they're at the edge. If so, no more scrolling past that point, otherwise follow player fully
