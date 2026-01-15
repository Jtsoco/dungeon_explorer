from enums.entity_enums import EntityType as ET, BoundaryType as BT, CollisionEntityTarget as CET, WeaponCategory as WC
from events_commands.events import BoundaryCollisionEvent as BCE, NewlyLoadedCellsEvent as NLCE, DeathEvent
from boundaries.boundary import Boundary
from entity.entity_data import EntityData
from animations.sprite_registry import SPRITES, BOSS_SPRITES
from entity.animation_data import AnimationData
from attack.weapon_data import WeaponData
from entity.entity_setup import spawn_weapon, spawn_winged_boss
from base_manager import BaseManager
from events_commands.commands import LoadMultipleEntityCollisionCommand as LMECC, LoadMultipleBoundariesCollisionCommand as LMBCC, LoadEntityCollisionCommand as LECC, LoadActiveAttackCollisionCommand as LAACC, LoadItemCommand, LoadItemCollisionCommand
import pyxel
from entity.entity_setup import spawn_weapon

class CellManager(BaseManager):
    def __init__(self, cells_data, active_cell: tuple, context):
        super().__init__(context=context)
        # TODO clean up and rework this class, won't have single cell manager any more so consolidate to one cell manager, as original design has changed for the game and also context by itself provides all the necessary data so only need one argument
        self.logic_manager = CellLogicManager()
        # cells is just a dict of cell coordinates to cell data, but the data is unloaded until needed
        self.cells = cells_data
        self.context = context

        # wait, what am i doing with single cell manager?? relook at this, change it, its really just a loader for a single cell...
        self.current_state = MultipleCellManager(self.cells[active_cell], self.cells, context)


    def setup_bus(self):
        self.context.bus.register_event_listener(BCE, self)
        self.context.bus.register_event_listener(DeathEvent, self)
        self.context.bus.register_command_listener(LoadItemCommand, self)


    def draw(self):
        self.current_state.draw()

    def handle_event(self, event):
        match event:
            case BCE():
                # boundary collision event
                # for now i'll just switch to purely using multiple cell manager, decide camera stuff later this is to get minimum viable done quick
                self.current_state.handle_boundary_event(event)

            case DeathEvent():
                self.current_state.remove_entity(event.entity)


    def handle_command(self, command):
        match command:
            case LoadItemCommand():
                self.load_item(command)

    def load_item(self, command):
        if command.load:
            item = command.item
            cell_coords = item.cell_pos
            if cell_coords in self.cells:
                cell = self.cells[cell_coords]
                cell.items.add(item)
                self.context.bus.send_command(LoadItemCollisionCommand(load=True, item=item))
        else:
            item = command.item
            cell_coords = item.cell_pos
            if cell_coords in self.cells:
                cell = self.cells[cell_coords]
                if item in cell.items:
                    cell.items.remove(item)
                    self.context.bus.send_command(LoadItemCollisionCommand(load=False, item=item))
        # else, item is in a cell that doesn't exist? ignore for now

class SingleCellManager():
    def __init__(self, cell_data):
        self.parent = None
        self.logic_manager = None
        self.set_cell(cell_data)
        self.active_cell = cell_data

    def get_active(self):
        return self.active_cell

    def get_boundaries(self):
        return self.active_cell.x_boundaries.union(self.active_cell.y_boundaries)

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
        enemies = set()
        start_x, start_y = cell_data.cell_x * 16, cell_data.cell_y * 16
        # honestly would be best to use context but for now this won't change so whatever, make it quick for now refactor later if needs change
        entity_types = set()
        x_boundaries = set()
        y_boundaries = set()
        for brick_x in range(start_x, start_x + 16):
            for brick_y in range(start_y, start_y + 16):
                tile = pyxel.tilemaps[0].pget(brick_x, brick_y)
                if tile in ET:
                    match tile:
                        # TODO consolidate all of this into an easier to manage  method/module/mapping later
                        case ET.SKULL.value:
                            animation_data = AnimationData(SPRITES[ET.SKULL])
                            # honestly could probably share the animation frames between all entities, this is fine for now but maybe change later
                            enemy_data = EntityData(entity_type=ET.SKULL, position=[brick_x * 8, brick_y * 8], animation_data=animation_data, cell_pos=(cell_data.cell_x, cell_data.cell_y), touch_damage=10)
                            enemies.add(enemy_data)
                            if ET.SKULL not in entity_types:
                                entity_types.add(ET.SKULL)
                        case ET.KNIGHT.value:
                            animation_data = AnimationData(SPRITES[ET.KNIGHT])
                            weapon_data = spawn_weapon(WC.ENEMY_SWORD)
                            enemy_data = EntityData(entity_type=ET.KNIGHT, position=[brick_x * 8, brick_y * 8], animation_data=animation_data, weapon_data=weapon_data, cell_pos=(cell_data.cell_x, cell_data.cell_y), touch_damage=0, health=150)
                            enemies.add(enemy_data)
                            if ET.KNIGHT not in entity_types:
                                entity_types.add(ET.KNIGHT)
                        case ET.WINGED_KNIGHT.value:
                            enemy = spawn_winged_boss((cell_data.cell_x, cell_data.cell_y), brick_x, brick_y, BOSS_SPRITES)
                            enemies.add(enemy)
                            if ET.WINGED_KNIGHT not in entity_types:
                                entity_types.add(ET.WINGED_KNIGHT)
                if tile in BT:
                    match tile:
                        case BT.X.value:
                            boundary = Boundary(BT.X, position=(brick_x * 8, brick_y * 8))
                            x_boundaries.add(boundary)
                        case BT.Y.value:
                            boundary = Boundary(BT.Y, position=(brick_x * 8, brick_y * 8))
                            y_boundaries.add(boundary)



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
    def __init__(self, cell_data, cells, context):
        self.cells = cells
        self.context = context
        self.center_cell = cell_data
        # adjacent, newly_loaded = self.handle_loading([cell_data])
        self.adjacent = set()
        self.load_cell(cell_data)
        self.central_cells = set()
        cell_data_to_set = set()
        cell_data_to_set.add(cell_data)
        self.set_active_cells(cell_data_to_set)
        # self.central_cells = [cell_data]
        self.context = context
        self.bus = context.bus


    def all_cells_loaded(self):
        return self.central_cells.union(self.adjacent)


    def determine_adjacent_cells(self, cell):
        x, y = cell.cell_x, cell.cell_y
        adjacent = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y)
        ]
        adjacent_cells = set()
        for cell in adjacent:
            if cell not in self.cells:
                continue
            else:
                adjacent_cells.add(self.cells[cell])


        return adjacent_cells

    def load_cells(self, cells):
        for cell in cells:
            if not cell.loaded:
                self.load_cell(cell)

    def handle_boundary_event(self, event):
        boundary = event.boundary
        cell_half_width = 8 * 16 // 2
        entity_cell = self.determine_cell(event.entity.rect.position)

        new_active_cell_coordinates = set()
        match boundary.boundary_type:
            case BT.X:
                if event.entity.rect.position[0] < (entity_cell[0] * 16 * 8) + cell_half_width:
                    # left boundary
                    new_active_cell_coordinates = [(entity_cell[0] - 1, entity_cell[1]), entity_cell]
                else:
                    # right boundary
                    new_active_cell_coordinates = [entity_cell, (entity_cell[0] + 1, entity_cell[1])]
            case BT.Y:
                if event.entity.rect.position[1] < (entity_cell[1] * 16 * 8) + cell_half_width:
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
        new_active_cells = set()
        for cell_coords in new_active_cell_coordinates:
            new_active_cells.add(self.cells[cell_coords])

        newly_loaded = self.set_active_cells(new_active_cells)
        if newly_loaded:
            # if cells were loaded, they were returned here
            self.context.bus.send_event(NLCE(loaded_cells=newly_loaded))




    def set_active_cells(self, active_cells):
        if active_cells == self.central_cells:
            return set()
        # we don't change anything, still same cells
        else:
            adjacent, newly_loaded = self.handle_loading(active_cells)
            # set the new cells
            old_cells = self.central_cells.union(self.adjacent)
            new_cells = active_cells.union(adjacent)
            enemies = self.enemies_to_load(old_cells, new_cells)
            boundaries = self.boundaries_to_load(self.central_cells, active_cells)
            items = self.items_to_load(old_cells, new_cells)

            if enemies or boundaries or items:
                # if enemies are newly loaded boundaries should have something newly loaded too and vice versa
                self.context.bus.send_command(LMECC(load=True, entities=enemies))
                self.context.bus.send_command(LMBCC(load=True, boundaries=boundaries))
                for item in items:
                    self.context.bus.send_command(LoadItemCollisionCommand(load=True, item=item))


            enemies = self.enemies_to_unload(old_cells, new_cells)
            boundaries = self.boundaries_to_unload(self.central_cells, active_cells)
            items = self.items_to_unload(old_cells, new_cells)

            if enemies or boundaries:
                self.context.bus.send_command(LMECC(load=False, entities=enemies))
                self.context.bus.send_command(LMBCC(load=False, boundaries=boundaries))
                for item in items:
                    self.context.bus.send_command(LoadItemCollisionCommand(load=False, item=item))



            self.central_cells = active_cells
            self.adjacent = adjacent - self.central_cells
            if newly_loaded:
                return newly_loaded
            # if new cells were loaded, inform whatever called this method
        return set()

    def all_to_load(self, old_cells, new_cells):
        enemies = set()
        boundaries = set()
        items = set()
        # should only ever be max 8 cells to iterate through
        for cell in new_cells:
            if cell not in old_cells:
                enemies.update(cell.get_enemies())
                boundaries.update(cell.get_boundaries())
                items.update(cell.get_items())
        return enemies, boundaries, items

    def all_to_unload(self, old_cells, new_cells):
        enemies = set()
        boundaries = set()
        items = set()
        # should only ever be max 8 cells to iterate through
        for cell in old_cells:
            if cell not in new_cells:
                enemies.update(cell.get_enemies())
                boundaries.update(cell.get_boundaries())
                items.update(cell.get_items())
        return enemies, boundaries, items

    def boundaries_to_load(self, old_cells, new_cells):
        items = set()
        # should only ever be max 8 cells to iterate through
        for cell in new_cells:
            if cell not in old_cells:
                items.update(cell.get_boundaries())
        return items

    def boundaries_to_unload(self, old_cells, new_cells):
        # should only ever be max 8 cells to iterate through
        items = set()
        for cell in old_cells:
            if cell not in new_cells:
                items.update(cell.get_boundaries())
        return items

    def enemies_to_load(self, old_cells, new_cells):
        enemies = set()
        # should only ever be max 8 cells to iterate through
        for cell in new_cells:
            if cell not in old_cells:
                enemies.update(cell.get_enemies())
        return enemies

    def enemies_to_unload(self, old_cells, new_cells):
        # should only ever be max 8 cells to iterate through
        enemies = set()
        for cell in old_cells:
            if cell not in new_cells:
                enemies.update(cell.get_enemies())
        return enemies

    def items_to_load(self, old_cells, new_cells):
        items = set()
        # should only ever be max 8 cells to iterate through
        for cell in new_cells:
            if cell not in old_cells:
                items.update(cell.get_items())
        return items

    def items_to_unload(self, old_cells, new_cells):
        # should only ever be max 8 cells to iterate through
        items = set()
        for cell in old_cells:
            if cell not in new_cells:
                items.update(cell.get_items())
        return items

    def get_boundaries(self):
        return self.get_active_boundaries()

    def get_active_boundaries(self):
        boundaries = set()
        for cell in self.central_cells:
            boundaries.update(cell.get_boundaries())
        return boundaries

    def get_central_enemies(self):
        enemies = set()
        for cell in self.central_cells:
            enemies.update(cell.get_enemies())
        return enemies

    def get_all_enemies(self):
        enemies = set()
        for cell in self.central_cells:
            enemies.update(cell.get_enemies())
        for cell in self.adjacent:
            enemies.update(cell.get_enemies())
        return enemies

    def get_enemies(self):
        return self.get_all_enemies()

    def get_adjacent_enemies(self):
        enemies = set()
        for cell in self.adjacent:
            enemies.update(cell.get_enemies())
        return enemies

    def get_active(self):
        return self.central_cells.union(self.adjacent)

    def get_items(self):
        items = set()
        for cell in self.central_cells:
            items.update(cell.get_items())
        for cell in self.adjacent:
            items.update(cell.get_items())
        return items
    def handle_loading(self, active_cells):
        adjacent_cells = set()
        newly_loaded = set()
        for cell in active_cells:
            adjacent_cells.update(self.determine_adjacent_cells(cell))
        # remove duplicates from adjacent_cells, and active cells
        adjacent_cells = set(adjacent_cells) - set(active_cells)
        # active cells should already be loaded
        for cell in adjacent_cells:
            if not cell.loaded:
                self.load_cell(cell)
                newly_loaded.add(cell)
        return adjacent_cells, newly_loaded

    def determine_cell(self, position):
        x, y = position
        cell_x = int(x // (16 * 8))
        cell_y = int(y // (16 * 8))
        return (cell_x, cell_y)

    def get_entity_types(self):
        entity_types = set()
        for cell in self.central_cells:
            for et in cell.entity_types:
                if et not in entity_types:
                    entity_types.add(et)
        for cell in self.adjacent:
            for et in cell.entity_types:
                if et not in entity_types:
                    entity_types.add(et)
        return entity_types

    def remove_entity(self, entity):
        all_cells = self.all_cells_loaded()
        for cell in all_cells:
            if entity in cell.enemies:
                cell.enemies.remove(entity)
                self.context.bus.send_command(LECC(load=False, entity=entity))
                # need to unload weapons too

                # i could make a group type class like pygame does, but i do kind of like the explicitness of this, like you know exactly where things are being removed from based on the event or command
                return
