
import pyxel
from startup_context import StartupContext
from cell_manager import CellManager
from scene_manager import SceneManager

class Game():
    def __init__(self):
    # need bus for communication between game systems
    # need camera system
    # need player system, divided into controller, player data, and player logic, and rendering
    # need active cell state machine, which will have states for normal cell (1 cell) and transitioning (2 cells)
    # need camera class to decide where the camera is based on active cell state, only updating when cell changes or during transition
    # possible could make an update array, and the camera class adds itself and moves out depending on whether it needs to handle a transition or not

    # anyway, start with just getting a camera and active cell (1 cell, no transitions) working first
        self.context = StartupContext()
        self.context.get_context()
        self.game_world = self.context.get_world()
        # the game world is a dict of cells

        self.cell_manager = CellManager(self.game_world, self.context.start_cell)
        self.scene_manager = SceneManager(self.context)

    def update(self):
        pass

    def draw(self):
        self.scene_manager.draw()
