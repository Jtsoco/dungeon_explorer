from enums.entity_enums import EntityType as ET, BoundaryType as BT
from events_commands.events import BoundaryCollisionEvent as BCE, NewlyLoadedCellsEvent as NLCE
from boundaries.boundary import Boundary
from entity.entity_data import EntityData
from animations.sprite_registry import SPRITES
from entity.animation_data import AnimationData
import pyxel

class CellManager():
    def __init__(self, cells_data, active_cell: tuple):
        self.logic_manager = CellLogicManager()
        self.cells = cells_data

        # wait, what am i doing with single cell manager?? relook at this, change it, its really just a loader for a single cell...
        self.current_state = MultipleCellManager(self.cells[active_cell], self.cells)

    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw()

    def handle_event(self, event):
        match event:
            case BCE():
                # boundary collision event
                # for now i'll just switch to purely using multiple cell manager, decide camera stuff later this is to get minimum viable done quick
                self.current_state.handle_boundary_event(event)

class SingleCellManager():
    def __init__(self, cell_data):
        self.parent = None
        self.logic_manager = None
        self.set_cell(cell_data)
        self.active_cell = cell_data

    def get_active(self):
        return self.active_cell

    def get_boundaries(self):
        return self.active_cell.x_boundaries + self.active_cell.y_boundaries

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
        enemies, entity_types, x_boundaries, y_boundaries = self.load_objects(cell_data)
        cell_data.enemies = enemies
        cell_data.entity_types = entity_types
        cell_data.x_boundaries = x_boundaries
        cell_data.y_boundaries = y_boundaries

    def remove_entity(self, entity):
        if entity in self.active_cell.enemies:
            self.active_cell.enemies.remove(entity)
            # for now just remove enemy, they're only referenced here and will be garbage collected

    def load_objects(self, cell_data):
        enemies = []
        start_x, start_y = cell_data.cell_x * 16, cell_data.cell_y * 16
        # honestly would be best to use context but for now this won't change so whatever, make it quick for now refactor later if needs change
        entity_types = []
        x_boundaries = []
        y_boundaries = []
        for brick_x in range(start_x, start_x + 16):
            for brick_y in range(start_y, start_y + 16):
                tile = pyxel.tilemaps[0].pget(brick_x, brick_y)
                if tile in ET:
                    match tile:
                        case ET.SKULL.value:
                            animation_data = AnimationData(SPRITES[ET.SKULL])
                            # honestly could probably share the animation frames between all entities, this is fine for now but maybe change later
                            enemy_data = EntityData(entity_type=ET.SKULL, position=[brick_x * 8, brick_y * 8], animation_data=animation_data, cell_pos=(cell_data.cell_x, cell_data.cell_y), touch_damage=10)
                            enemies.append(enemy_data)
                            if ET.SKULL not in entity_types:
                                entity_types.append(ET.SKULL)
                if tile in BT:
                    match tile:
                        case BT.X.value:
                            boundary = Boundary(BT.X, position=(brick_x * 8, brick_y * 8))
                            x_boundaries.append(boundary)
                        case BT.Y.value:
                            boundary = Boundary(BT.Y, position=(brick_x * 8, brick_y * 8))
                            y_boundaries.append(boundary)



        return enemies, entity_types, x_boundaries, y_boundaries



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

class MultipleCellManager(SingleCellManager):
    def __init__(self, cell_data, cells):
        self.cells = cells
        self.center_cell = cell_data
        adjacent, newly_loaded = self.handle_loading([cell_data])
        self.adjacent = adjacent
        self.load_cell(cell_data)
        self.central_cells = [cell_data]



    def determine_adjacent_cells(self, cell):
        x, y = cell.cell_x, cell.cell_y
        adjacent = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y)
        ]
        adjacent_cells = []
        for cell in adjacent:
            if cell not in self.cells:
                adjacent.remove(cell)
            else:
                adjacent_cells.append(self.cells[cell])

        return adjacent_cells

    def load_cells(self, cells):
        for cell in cells:
            if not cell.loaded:
                self.load_cell(cell)

    def handle_boundary_event(self, event):
        boundary = event.boundary
        cell_half_width = 8 * 16 // 2
        entity_cell = self.determine_cell(event.entity.position)

        new_active_cell_coordinates = []
        match boundary.boundary_type:
            case BT.X:
                if event.entity.position[0] < (entity_cell[0] * 16 * 8) + cell_half_width:
                    # left boundary
                    new_active_cell_coordinates = [(entity_cell[0] - 1, entity_cell[1]), entity_cell]
                else:
                    # right boundary
                    new_active_cell_coordinates = [entity_cell, (entity_cell[0] + 1, entity_cell[1])]
            case BT.Y:
                if event.entity.position[1] < (entity_cell[1] * 16 * 8) + cell_half_width:
                    # top boundary
                    new_active_cell_coordinates = [(entity_cell[0], entity_cell[1] - 1), entity_cell]
                else:
                    # bottom boundary
                    new_active_cell_coordinates = [entity_cell, (entity_cell[0], entity_cell[1] + 1)]
        # if new active cells are current central cells, do nothing
        # else, take take new active cells, load any not currently loaded
        # skipping any active cells already in central cells
        # then, get adjacent cells for new active cells, load any not currently loaded
            # this should load 8 cells max, 2 active 6 adjacent
            # consider optimization later if necessary, for now get minimum viable out
        new_active_cells = []
        for cell_coords in new_active_cell_coordinates:
            new_active_cells.append(self.cells[cell_coords])
        events = []
        if self.set_active_cells(new_active_cells):
            # if cells were loaded, they were returned here
            events.append(NLCE(loaded_cells=events))
        return events



    def set_active_cells(self, active_cells):
        if set(active_cells) == set(self.central_cells):
            return False
        # we don't change anything, still same cells
        else:
            adjacent, newly_loaded = self.handle_loading(active_cells)
            # set the new cells
            self.central_cells = active_cells
            self.adjacent = list(set(adjacent) - set(self.central_cells))
            if newly_loaded:
                return newly_loaded
            # if new cells were loaded, inform whatever called this method
        return False

    def get_boundaries(self):
        return self.get_active_boundaries()

    def get_active_boundaries(self):
        boundaries = []
        for cell in self.central_cells:
            boundaries.extend(cell.get_boundaries())
        return boundaries

    def get_central_enemies(self):
        enemies = []
        for cell in self.central_cells:
            enemies.extend(cell.get_enemies())
        return enemies

    def get_all_enemies(self):
        enemies = []
        for cell in self.central_cells:
            enemies.extend(cell.get_enemies())
        for cell in self.adjacent:
            enemies.extend(cell.get_enemies())
        return enemies

    def get_enemies(self):
        return self.get_all_enemies()

    def get_adjacent_enemies(self):
        enemies = []
        for cell in self.adjacent:
            enemies.extend(cell.get_enemies())
        return enemies

    def get_active(self):
        return self.central_cells + self.adjacent

    def handle_loading(self, active_cells):
        adjacent_cells = []
        newly_loaded = []
        for cell in active_cells:
            adjacent_cells.extend(self.determine_adjacent_cells(cell))
        # remove duplicates from adjacent_cells, and active cells
        adjacent_cells = list(set(adjacent_cells) - set(active_cells))
        # active cells should already be loaded
        for cell in adjacent_cells:
            if not cell.loaded:
                self.load_cell(cell)
                newly_loaded.append(cell)
        return adjacent_cells, newly_loaded

    def determine_cell(self, position):
        x, y = position
        cell_x = x // (16 * 8)
        cell_y = y // (16 * 8)
        return (cell_x, cell_y)

    def get_entity_types(self):
        entity_types = []
        for cell in self.central_cells:
            for et in cell.entity_types:
                if et not in entity_types:
                    entity_types.append(et)
        for cell in self.adjacent:
            for et in cell.entity_types:
                if et not in entity_types:
                    entity_types.append(et)
        return entity_types

    def remove_entity(self, entity):
        for cell in self.central_cells:
            if entity in cell.enemies:
                cell.enemies.remove(entity)
                return
