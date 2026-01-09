
import pyxel
from cell_manager import CellManager
from scene_manager import SceneManager
from debug.quick_debug import display_info, quick_point, outline_entity, calculate_fps
from entity.entity_manager import EntityManager
from collisions.collision_manager import CollisionManager
from combat.damage_manager import DamageManager
from entity.entity_setup import spawn_player

from events_commands.events import PossibleAttackCollisionEvent as PACE, DamageEvent as DE, PhysicsEvent as PE, DeathEvent as Death, NewlyLoadedCellsEvent as NLCE, BoundaryCollisionEvent as BCE
from events_commands.commands import EffectCommand, SoundCommand, MusicCommand, AudioCommand
from HUD.hud_manager import HUDManager

from effects.effects_manager import EffectsManager
from audio.sound_effects_manager import SoundEffectsManager

from system.context import Context

from datetime import datetime
class Game():
    def __init__(self):
    # need bus for communication between game systems
    # need camera system
    # need player system, divided into controller, player data, and player logic, and rendering
    # need active cell state machine, which will have states for normal cell (1 cell) and transitioning (2 cells)
    # need camera class to decide where the camera is based on active cell state, only updating when cell changes or during transition
    # possible could make an update array, and the camera class adds itself and moves out depending on whether it needs to handle a transition or not

    # anyway, start with just getting a camera and active cell (1 cell, no transitions) working first
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
        self.player_data = spawn_player()
        # for now player is just stored here, later might make a separate player manager if needed
        self.player_data.rect.position = [self.context.data_context.player_start[0] * self.context.data_context.BRICK_SIZE, self.context.data_context.player_start[1] * self.context.data_context.BRICK_SIZE]
        self.scene_manager.camera.set_target(self.player_data.rect)

        # just have it use players attack and animation manager for now, as they work, restructure later if needed
        self.entity_manager = EntityManager(context=self.context)
        types = self.cell_manager.current_state.get_entity_types()
        self.entity_manager.setup_entity(self.player_data.entity_type)
        self.entity_manager.setup_entities(types)
        # just this quick one for now on setting up entities, refactor later when redoing cell loading system
        self.collision_manager.player = self.player_data

        self.damage_manager = DamageManager(self.context)


        # debug for framerate
        self.last_time = datetime.now()
        self.current_time = datetime.now()
        self.last_frame_count = 0
        self.current_frame_count = 0
        self.context.data_context.player_data = self.player_data

        self.effects_manager = EffectsManager(self.context)
        self.sound_effects_manager = SoundEffectsManager(self.context)
        self.sound_effects_manager.handle_command(MusicCommand(music_enum=0))  # Start background music

        self.hud_manager = HUDManager(self.context)



    def update(self):
        all_entities = self.cell_manager.current_state.get_enemies() + [self.player_data]
        main_commands = []
        for entity in all_entities:
            self.entity_manager.update_entity(entity)


        # after main events, need a last check to see if any state changes happend that need to be handled for respective entities
        # possibly consider breaking down entity manager into subparts or having it like this for now where it contains a full 'sub process' for each entity

        # take these main event filter logic type code sections and put them into a deticated filter module/class later, to clean this logic up

            # match event:
            #     case PACE():
            #         self.collision_manager.register_collision(event)
        for command in main_commands:
            self.delegate_command(command)


        self.collision_manager.update()
        self.effects_manager.update()
        self.damage_manager.update()
        self.cell_manager.update()
        self.entity_manager.update()
        self.hud_manager.update()

        self.sound_effects_manager.update()
        self.scene_manager.camera.update()



        # for now all main events are collision, refactor for sound later

        # then, do damage manager,
        # get events from damage manager,
        # for now if death event remove from entities, make death animation later
        # for physics pass to entity physics manager through event handler and it will handle add momentum event, and add momentum, which will update position on next physics update (next frame then), but update entities momentum now.
        # also edit physics manager, so that if momentum is above/below current speed based on direction, change by 1 until it matches that speed. revist eventually later for more robust acceleration/deceleration system

    def delegate_command(self, command):
        # for now commands probably shouldn't return new events or commands, but if they do in the future can handle that here
        match command:
            case EffectCommand():
                self.effects_manager.handle_command(command)
            case AudioCommand():
                self.sound_effects_manager.handle_command(command)

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

    def draw(self):
        self.scene_manager.draw()
        effects = self.effects_manager.get_effects()
        self.scene_manager.render_effects(effects)
        # for now this, but change it later when i have time
        enemies = self.cell_manager.current_state.get_enemies()
        for enemy in enemies:
            self.entity_manager.draw(enemy)
        self.entity_manager.draw(self.player_data)
        camera_pos = self.scene_manager.camera.current_camera
        display_info(f"Player Pos: {self.player_data.position[0]}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+8)

        self.scene_manager.set_camera_to_zero()
        self.hud_manager.draw()
        self.scene_manager.set_camera_to_current()
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
        fps = calculate_fps(self.last_time, self.current_time, self.last_frame_count, self.current_frame_count)
        self.last_time = self.current_time
        self.last_frame_count = self.current_frame_count
        # display_info(fps, pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+2)
