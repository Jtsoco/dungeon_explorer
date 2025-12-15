
import pyxel
from startup_context import StartupContext
from cell_manager import CellManager
from scene_manager import SceneManager
from player.player_entity import PlayerEntity
from debug.quick_debug import display_info, quick_point, outline_entity, calculate_fps
from entity.entity_manager import EntityManager
from collisions.collision_manager import CollisionManager
from combat.damage_manager import DamageManager

from events_commands.events import PossibleAttackCollisionEvent as PACE, DamageEvent as DE, PhysicsEvent as PE

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
        self.context = StartupContext()
        self.context.get_context()
        self.game_world = self.context.get_world()
        # the game world is a dict of cells

        self.cell_manager = CellManager(self.game_world, self.context.start_cell)
        self.scene_manager = SceneManager(self.context)
        self.player = PlayerEntity(self.context)
        # for now player is just stored here, later might make a separate player manager if needed

        # just have it use players attack and animation manager for now, as they work, restructure later if needed
        self.entity_manager = EntityManager(self.player.animation_manager, self.player.attack_manager, self.context)
        types = self.cell_manager.current_state.active_cell.entity_types
        self.entity_manager.setup_entities(types)
        # just this quick one for now on setting up entities, refactor later when redoing cell loading system
        self.collision_manager = CollisionManager()

        self.damage_manager = DamageManager()

        # debug for framerate
        self.last_time = datetime.now()
        self.current_time = datetime.now()
        self.last_frame_count = 0
        self.current_frame_count = 0

    def update(self):
        main_events = []
        for enemy in self.cell_manager.current_state.get_enemies():
            events = self.entity_manager.update(enemy)
            main_events.extend(events)
        events = self.player.update()
        main_events.extend(events)
        # after main events, need a last check to see if any state changes happend that need to be handled for respective entities
        # possibly consider breaking down entity manager into subparts or having it like this for now where it contains a full 'sub process' for each entity

        # take these main event filter logic type code sections and put them into a deticated filter module/class later, to clean this logic up
        for event in main_events:
            match event:
                case PACE():
                    self.collision_manager.register_collision(event)
        collision_events = self.collision_manager.update(self.player.data, self.cell_manager.current_state.get_enemies())

        events = collision_events
        while events:
            event = events.pop(0)
            new_events = self.delegate_event(event)
            events.extend(new_events)




        # for now all main events are collision, refactor for sound later

        # then, do damage manager,
        # get events from damage manager,
        # for now if death event remove from entities, make death animation later
        # for physics pass to entity physics manager through event handler and it will handle add momentum event, and add momentum, which will update position on next physics update (next frame then), but update entities momentum now.
        # also edit physics manager, so that if momentum is above/below current speed based on direction, change by 1 until it matches that speed. revist eventually later for more robust acceleration/deceleration system

    def delegate_event(self, event):
        events = []
        match event:
            case DE():
                new_events = self.damage_manager.handle_event(event)
                events.extend(new_events)
            case PE():
                new_events = self.entity_manager.handle_event(event)
                events.extend(new_events)
        return events

    def draw(self):
        self.scene_manager.draw()
        # for now this, but change it later when i have time
        enemies = self.cell_manager.current_state.get_enemies()
        for enemy in enemies:
            self.player.renderer.render(enemy)
        self.player.draw()
        camera_pos = self.scene_manager.camera.current_camera
        # display_info(f"Player Pos: {self.player.data.position}", pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+2)
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
        display_info(fps, pos_x=camera_pos[0]+2, pos_y=camera_pos[1]+2)
