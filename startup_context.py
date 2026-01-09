import pyxel
from cell_data import CellData
from system.tile_context import TileContext
from enums.entity_enums import EntityType as ET
from cell_data import CellData
class StartupContext():
    def __init__(self):
        # size in cells
        self.tile_map = 0
        self.player_start = (0, 0)

        self.tile_context = TileContext(self.tile_map)
        # player start is tuple, containing brick x and brick y
        self.ENEMY_SPAWNS = {(0, 15): ET.SKULL}
        self.cell_x = 3
        self.cell_y = 2
        self.TRANSPARENT_COLOR = 2
        self.TILE_SPAWN1 = None
        self.TILE_SPAWN2 = None
        self.PLAYER_SPAWN = (3, 10)
        self.BORDER_TRANSITION_X = (3, 8)
        self.BORDER_TRANSITION_Y = (3, 9)
        self.BRICK_SIZE = 8  # 8 x 8 pixels
        self.CELL_SIZE = 16  # 16 x 16 bricks
        self.game_world = {}
        self.start_cell = (0,0)
        self.collideable_tile_x = 4
        # anything greater than or equal to this tile number is collideable

        # can be more than one active cell at a time for transitions
        self.player_data = None

    def get_context(self):
        self.check_cells()
        # for bigger games, consider lazy loading where once player cell is found, only load nearby cells
        # but honestly this is for dungeons and each should be small, so this should work fine as is

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
