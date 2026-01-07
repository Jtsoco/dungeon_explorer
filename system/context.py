# this will hold the context, which holds the bus and other necessary systems needed throughout the game, like map info and such
import pyxel
from system.tile_context import TileContext
from cell_data import CellData

class Context():
    def __init__(self):
        self.bus = None
        self.data_context = None
        self.tile_context = None

    def set_bus(self, bus):
        self.bus = bus

    def set_data_context(self, data_context):
        self.data_context = data_context

    def get_bus(self):
        return self.bus

    def get_data_context(self):
        return self.data_context

    def setup_tile_context(self):
        if not self.data_context:
            raise ValueError("Data context must be set before setting up tile context.")
        self.tile_context = TileContext(self.data_context.tile_map,
                                        brick_size=self.data_context.BRICK_SIZE,
                                        cell_size=self.data_context.CELL_SIZE)

    def setup_defaults(self):
        self.data_context = DataContext()
        self.data_context.check_cells()
        self.setup_tile_context()


class DataContext():
    def __init__(self):
        # map info
        self.tile_map = 0  # default tile map index
        self.BRICK_SIZE = 8
        self.CELL_SIZE = 16

        self.player_start = (0, 0)
        self.start_cell = (0, 0)

        # location in tile map of player spawn indicator point
        self.PLAYER_SPAWN = (3, 10)

        # border transition indicators, helps to identify when player is at edge of cell and loading may need to occur
        self.BORDER_TRANSITION_X = (3, 8)
        self.BORDER_TRANSITION_Y = (3, 9)
        self.game_world = {}


        # anything greater than or equal to this tile number is collideable, and is used in tile context for determining whether a tile is collideable. x value comes from the tilemap x coordinate in the tile sheet
        self.collideable_tile_x = 4

        # these are just initial values, and determine just how far the map goes. For now, empty cell data for each cell will be loaded, scale of game is small and the cell data itself isn't large until enemies are loaded, so should be fine for now
        self.cell_x = 3
        self.cell_y = 2

        # the transparent color for rendering
        self.TRANSPARENT_COLOR = 2

        # player data, as it's useful for enemies to know about
        self.player_data = None

    def get_world(self):
        return self.game_world

    def get_tile(self, x, y):
        return pyxel.tilemaps[0].pget(x, y)

    def check_cells(self):
        for cell_x in range(self.cell_x):
            for cell_y in range(self.cell_y):
                cell = CellData(cell_x, cell_y)
                self.game_world[(cell_x, cell_y)] = cell
                # maybe eventually set a color being in a corner to indicate a cell isn't to be iterated over, so i can skip it in the future
                self.check_cell_tiles(cell_x, cell_y)


    def check_cell_tiles(self, cell_x, cell_y):
        start_x = cell_x * self.CELL_SIZE
        start_y = cell_y * self.CELL_SIZE
        for brick_x in range(start_x, start_x + self.CELL_SIZE):
            for brick_y in range(start_y, start_y + self.CELL_SIZE):
                self.check_brick(brick_x, brick_y)

    def check_brick(self, brick_x, brick_y):
        # check for spawn points and any item points necessary
        # it seems the map uses tiles counted by brick size
        # print(f"Checking brick at ({brick_x}, {brick_y}) for special tiles...")
        brick = pyxel.tilemaps[0].pget(brick_x, brick_y)
        # print(f"Brick at ({brick_x}, {brick_y}) has tile {brick}")
        match brick:
            case self.PLAYER_SPAWN:
                self.player_start = (brick_x, brick_y)
                cell = self.find_cell(brick_x * self.BRICK_SIZE, brick_y * self.BRICK_SIZE)
                self.start_cell = cell



    def find_cell(self, x, y):
        # floor division with //
        brick_x = x // self.BRICK_SIZE
        brick_y = y // self.BRICK_SIZE
        cell_x = brick_x // self.CELL_SIZE
        cell_y = brick_y // self.CELL_SIZE
        return (cell_x, cell_y)
