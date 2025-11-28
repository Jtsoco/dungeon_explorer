import pyxel

# for now, this is just a module of functions that take in data and return info about tiles
class TileContext():
    def __init__(self, tile_map, brick_size=8, cell_size=16):
        self.tile_map = tile_map
        # tile map is just the number of the tile map in pyxel tilemaps
        self.BRICK_SIZE = brick_size
        self.CELL_SIZE = cell_size

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

    def get_touching_bricks(self, x, y, w, h):
        # x, y, w, h, are pyxel coordinates and square size
        bricks = set()
        # some bricks can be duplicates, as they are images at coordinates x,y
        # this basically just says what bricks are being touched by this rectangle
        # maybe it would be better to return a list of brick coordinates instead, and just check if touching those? that way its not needed to get touching bricks all the time
        # eh both have uses, implement both quick see how it goes
        # this method probably will have some uses itself
        # it's quick to implement anyway, the other requires making a rect class. Use for now, test speed of method later
        start_brick_x = x // self.BRICK_SIZE
        start_brick_y = y // self.BRICK_SIZE
        end_brick_x = (x + w - 1) // self.BRICK_SIZE
        end_brick_y = (y + h - 1) // self.BRICK_SIZE
        for brick_x in range(start_brick_x, end_brick_x + 1):
            for brick_y in range(start_brick_y, end_brick_y + 1):
                bricks.add((self.get_brick(brick_x, brick_y)))

        return bricks
