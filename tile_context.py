import pyxel

# for now, this is just a module of functions that take in data and return info about tiles
class TileContext():
    def __init__(self, tile_map, brick_size = 8, cell_size = 16):
        self.BRICK_SIZE = brick_size
        self.CELL_SIZE = cell_size
        self.tile_map = tile_map

    def get_brick_by_pixel(self, x, y):
        brick_x = x // self.BRICK_SIZE
        brick_y = y // self.BRICK_SIZE
        brick = pyxel.tilemaps[0].pget(brick_x, brick_y)
        return brick

    def get_brick(self, brick_x, brick_y):
        return pyxel.tilemaps[0].pget(brick_x, brick_y)

    def get_surrounding_bricks(self, x, y):
        # x and y are pixel coordinates
        brick_x = x // self.BRICK_SIZE
        brick_y = y // self.BRICK_SIZE
        bricks = {}
        # get all bricks in 9x9 area centered on brick_x, brick_y
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                bx = brick_x + dx
                by = brick_y + dy
                bricks[(bx, by)] = self.get_brick(bx, by)
        # remove center brick
        bricks.pop((brick_x, brick_y), None)
        return bricks

    def get_brick_number(self, x, y):
        # x and y are pixel coordinates
        brick_x = x // self.BRICK_SIZE
        brick_y = y // self.BRICK_SIZE
        return (brick_x, brick_y)
