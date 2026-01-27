
import pyxel
from cell_manager import CellManager
from scene_manager import SceneManager
from debug.quick_debug import display_info, quick_point, outline_entity, calculate_fps
from entity.entity_manager import EntityManager
from collisions.collision_manager import CollisionManager
from combat.damage_manager import DamageManager
from entity.entity_setup import spawn_player
from HUD.player_draw import shadow_text

from app_level.app_commands_events import StateChangeEvent as AppStateChangeEvent
from app_level.app_enums import MenuState

from events_commands.events import PossibleAttackCollisionEvent as PACE, DamageEvent as DE, PhysicsEvent as PE, DeathEvent as Death, NewlyLoadedCellsEvent as NLCE, BoundaryCollisionEvent as BCE, GameEvent as GE, GameOverEvent as GOE, GameClearEvent as GCE
from events_commands.commands import EffectCommand, SoundCommand, MusicCommand, AudioCommand
from HUD.hud_manager import HUDManager
from temporary_managers.powerup_manager import PowerupManager
from temporary_managers.item_manager import ItemManager
from effects.effects_manager import EffectsManager
from audio.sound_effects_manager import SoundEffectsManager
from system.context import Context

from datetime import datetime
class Game():
    def __init__(self, top_bus, player_data=None):
    # need bus for communication between game systems
    # need camera system
    # need player system, divided into controller, player data, and player logic, and rendering
    # need active cell state machine, which will have states for normal cell (1 cell) and transitioning (2 cells)
    # need camera class to decide where the camera is based on active cell state, only updating when cell changes or during transition
    # possible could make an update array, and the camera class adds itself and moves out depending on whether it needs to handle a transition or not

    # anyway, start with just getting a camera and active cell (1 cell, no transitions) working first
        # the upper bus exists to send events to app level, like during game over screen pressing enter to go back to menu
        self.top_bus = top_bus
        self.context = Context()
        self.context.setup_defaults()
        # adjust this later
        # self.context = StartupContext()
        # self.context.get_context()
        self.game_world = self.context.data_context.get_world()
        # the game world is a dict of cells

        self.collision_manager = CollisionManager(self.context)
        self.cell_manager = CellManager(self.game_world, self.context.data_context.start_cell, self.context)
        self.scene_manager = SceneManager(self.context)
        if player_data:
            self.context.data_context.player_data = player_data
        else:
            self.context.data_context.player_data = spawn_player()
        # for now player is just stored here, later might make a separate player manager if needed
        self.context.data_context.player_data.rect.position = [self.context.data_context.player_start[0] * self.context.data_context.BRICK_SIZE, self.context.data_context.player_start[1] * self.context.data_context.BRICK_SIZE]
        self.scene_manager.camera.set_target(self.context.data_context.player_data.rect)

        # just have it use players attack and animation manager for now, as they work, restructure later if needed
        self.entity_manager = EntityManager(context=self.context)
        types = self.cell_manager.current_state.get_entity_types()
        self.entity_manager.setup_entity(self.context.data_context.player_data.entity_type)
        self.entity_manager.setup_entities(types)
        # just this quick one for now on setting up entities, refactor later when redoing cell loading system
        self.collision_manager.player = self.context.data_context.player_data

        self.damage_manager = DamageManager(self.context)
        self.PowerupManager = PowerupManager(self.context)


        # debug for framerate
        self.last_time = datetime.now()
        self.current_time = datetime.now()
        self.last_frame_count = 0
        self.current_frame_count = 0
        self.context.data_context.player_data = self.context.data_context.player_data

        self.effects_manager = EffectsManager(self.context)
        self.sound_effects_manager = SoundEffectsManager(self.context)
        self.sound_effects_manager.handle_command(MusicCommand(music_enum=0))  # Start background music

        self.hud_manager = HUDManager(self.context)
        self.hud_manager.setup_player_hud(self.context.data_context.player_data)
        self.item_manager = ItemManager(self.context)
        self.current_update = self.regular_update

        self.context.bus.register_event_listener(GE, self)
        self.current_draw = self.regular_draw


    def update(self):
        self.current_update()

    def draw(self):
        self.current_draw()

    def regular_update(self):
        all_entities = self.cell_manager.current_state.get_enemies()
        all_entities.add(self.context.data_context.player_data)

        for entity in all_entities:
            self.entity_manager.update_entity(entity)

        self.collision_manager.update()
        self.effects_manager.update()
        self.damage_manager.update()
        self.cell_manager.update()
        self.entity_manager.update()
        self.hud_manager.update()

        self.sound_effects_manager.update()
        self.scene_manager.camera.update()


    def delegate_event(self, event):
        events = []
        # here it may be useful to have an observer pattern later, as a consideration for refactoring, but for now just this
        commands = []
        match event:
            case PE():
                new_events = self.entity_manager.handle_event(event)
                events.extend(new_events)
            case Death():
                self.death_event(event)
            case BCE():
                new_events = self.cell_manager.handle_event(event)
                events.extend(new_events)
            case NLCE():
                new_events = self.entity_manager.handle_newly_loaded_cells(event)
                events.extend(new_events)
        return events, commands

    def death_event(self, event):
        entity = event.entity
        if not entity.player:
            self.cell_manager.current_state.remove_entity(entity)
            self.effects_manager.handle_event(event)

    def no_entity_update(self):
        self.cell_manager.update()
        self.effects_manager.update()
        self.hud_manager.update()
        self.sound_effects_manager.update()
        self.scene_manager.camera.update()

    def regular_draw(self):
        self.scene_manager.set_camera_to_current()

        self.scene_manager.draw()
        effects = self.effects_manager.get_effects()
        # for now this, but change it later when i have time
        enemies = self.cell_manager.current_state.get_enemies()
        for enemy in enemies:
            self.entity_manager.draw(enemy)
        items = self.cell_manager.current_state.get_items()
        self.scene_manager.render_items(items)
        self.entity_manager.draw(self.context.data_context.player_data)
        self.scene_manager.render_effects(effects)
        camera_pos = self.scene_manager.camera.current_camera
        # display_info(f"Player Pos: {self.context.data_context.player_data.position[0]}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+8)

        # hud has no knowledge of world positions, so temporary set to 0,0 for drawing then set back
        self.scene_manager.set_camera_to_zero()
        self.hud_manager.draw()
        # outline_entity(self.player.data)

        # player animation
        # a_d = self.player.data.animation_data
        # display_info(f"Anim State: M-{self.player.data.movement_state.name} D-{self.player.data.direction_state.name}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+12)
        # display_info(f"Attack State: {self.player.data.action_state.name}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+17)
        # display_info(f"Attack frame: {self.player.data.weapon.current_frame}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+22)
        # display_info(f"Anim Frame: {a_d.current_frame}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+27)
        # display_info(f"Frame Pos: {a_d.get_current_frame().pos}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+32)
        self.current_time = datetime.now()
        self.current_frame_count = pyxel.frame_count
        # fps = calculate_fps(self.last_time, self.current_time, self.last_frame_count, self.current_frame_count)
        self.last_time = self.current_time
        self.last_frame_count = self.current_frame_count
        # display_info(fps, pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+2)
    def game_over_update(self):
        # maybe rename these and consolidate
        self.no_entity_update()

    def game_clear_update(self):
        self.regular_update()
        # let you play, but enter sends you back to start screen


    def game_over_draw(self):
        self.regular_draw()
        message = "Game Over!"
        position = (pyxel.width // 2 - 20, pyxel.height // 4)

        # pyxel.rect(position[0]-8, position[1]-8, pyxel.width // 2, 32, 0)
        shadow_text(position, message, color=0)
        pyxel.text(position[0], position[1], message, 7)
        message = "Press Enter"
        position = (position[0], pyxel.height // 3)
        shadow_text(position, message, color=0)
        pyxel.text(position[0], position[1], message, 7)

        # this is here, because putting it in update caused drawing issues, where the hole screen would go black and stay that way, so until i investigate the bug this will be the hotfix
        if pyxel.btnp(pyxel.KEY_RETURN):
            # send event to app level to switch to game over menu
            self.top_bus.send_event(AppStateChangeEvent(MenuState.MAIN_MENU))

    def game_clear_draw(self):
        # TODO consolidate game over and clear draw to same type of thing, just different message. Was just easier to copy for now
        self.regular_draw()
        message = "Game Clear!"
        position = (pyxel.width // 2 - 24, pyxel.height // 4)

        # pyxel.rect(position[0]-8, position[1]-8, pyxel.width // 2, 32, 0)
        shadow_text(position, message, color=0)
        pyxel.text(position[0], position[1], message, 7)
        message = "Press Enter"
        position = (position[0], pyxel.height // 3)
        shadow_text(position, message, color=0)
        pyxel.text(position[0], position[1], message, 7)

        # this is here, because putting it in update caused drawing issues, where the hole screen would go black and stay that way, so until i investigate the bug this will be the hotfix
        if pyxel.btnp(pyxel.KEY_RETURN):
            # send event to app level to switch to game over menu
            self.top_bus.send_event(AppStateChangeEvent(MenuState.MAIN_MENU))

    def notify_event(self, event):
        match event:
            case GOE():
                self.current_update = self.game_over_update
                self.current_draw = self.game_over_draw
            case GCE():
                self.current_update = self.game_clear_update
                self.current_draw = self.game_clear_draw
