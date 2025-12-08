class CellData():
    def __init__(self, cell_x, cell_y, context=None):
        self.context = context
        # might not actually need to pass context
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.border_x = []
        self.border_y = []
        self.enemies = []
        self.loaded = False

    def update(self):
        pass

    def draw(self):
        pass
        # draw enemies and items in the cell
        # not the cell background itself, as the camera handles that so screen transitions can happen
    # enemies will need to be aware of what cell they're in so they don't go beyond cell if possible

    def get_cell_coordinates(self):
        x = self.cell_x * 16 * 8
        y = self.cell_y * 16 * 8
        return (x, y)

    # methods to allow cells to message things when events happen?
    # or maybe just make cells primarily old data, and have some other manager do the updates through a cells respective things, like going through enemies in each cell and updating them.
    # data holder cell, or more active cell? maybe split cells into data cell and manager cell? that way data cells are simple holders, and managers handle logic
    # IMPORTANT: just have these be data cells
