from enums.entity_enums import EntityType as ET
from entity.entity_data import EntityData
from animations.animation_setup import skull_animation
from entity.animation_data import AnimationData
import pyxel

class CellManager():
    def __init__(self, cells_data, active_cell: tuple):
        self.logic_manager = CellLogicManager()
        self.cells = cells_data

        # wait, what am i doing with single cell manager?? relook at this, change it, its really just a loader for a single cell...
        self.current_state = SingleCellManager(self.cells[active_cell])

    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw()

class SingleCellManager():
    def __init__(self, cell_data):
        self.parent = None
        self.logic_manager = None
        self.set_cell(cell_data)
        self.active_cell = cell_data

    def get_active(self):
        return self.active_cell

    def set_logic_manager(self, logic_manager):
        self.logic_manager = logic_manager
    def set_parent(self, parent):
        self.parent = parent

    def set_cell(self, cell_data):
        if not cell_data.loaded:
            self.load_cell(cell_data)
            return True
        self.cell_data = cell_data
        return False

    def load_cell(self, cell_data):
        cell_data.loaded = True
        enemies, entity_types = self.load_enemies(cell_data)
        cell_data.enemies = enemies
        cell_data.entity_types = entity_types

    def load_enemies(self, cell_data):
        enemies = []
        start_x, start_y = cell_data.cell_x * 16, cell_data.cell_y * 16
        # honestly would be best to use context but for now this won't change so whatever, make it quick for now refactor later if needs change
        entity_types = []
        for brick_x in range(start_x, start_x + 16):
            for brick_y in range(start_y, start_y + 16):
                tile = pyxel.tilemaps[0].pget(brick_x, brick_y)
                if tile in ET:
                    match tile:
                        case ET.SKULL.value:
                            animation_data = AnimationData(skull_animation())
                            # honestly could probably share the animation frames between all entities, this is fine for now but maybe change later
                            enemy_data = EntityData(entity_type=ET.SKULL, position=[brick_x * 8, brick_y * 8], animation_data=animation_data, cell_pos=(cell_data.cell_x, cell_data.cell_y))
                            enemies.append(enemy_data)
                            if ET.SKULL not in entity_types:
                                entity_types.append(ET.SKULL)


        return enemies, entity_types



    def get_enemies(self):
        return self.active_cell.enemies

    def update(self):
        self.logic_manager.update(self.cell_data)
        # the multiple cell manager will handle updating multiple cells, using the same logic_manager handed to it.
    # nothing to update yet as no enemies within

    def draw(self):
        pass

    # nothing to draw yet as camera handles background



class CellLogicManager():
    def __init__(self):
        pass
