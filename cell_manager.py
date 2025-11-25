class CellManager():
    def __init__(self, cells_data, active_cell: tuple):
        self.logic_manager = CellLogicManager()
        self.cells = cells_data
        self.current_state = SingleCellManager(active_cell)

    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw()

class SingleCellManager():
    def __init__(self, cell_data):
        self.parent = None
        self.logic_manager = None
        self.cell_data = cell_data

    def set_logic_manager(self, logic_manager):
        self.logic_manager = logic_manager
    def set_parent(self, parent):
        self.parent = parent

    def update(self):
        self.logic_manager.update(self.cell_data)
        # the multiple cell manager will handle updating multiple cells, using the same logic_manager handed to it.
        pass
    # nothing to update yet as no enemies within

    def draw(self):
        pass
    # nothing to draw yet as camera handles background



class CellLogicManager():
    def __init__(self):
        pass
