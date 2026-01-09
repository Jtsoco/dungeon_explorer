from animations.animation_manager import AnimationManager
from attack.attack_manager import AttackManager
from events_commands.commands import MovementCommand, AttackCommand, EffectCommand, SoundCommand, AudioCommand, PhysicsCommand
from events_commands.events import StateChangedEvent, PossibleCollisionEvent as PCE, AttackFinishedEvent as AFE, PhysicsEvent as PE, NewlyLoadedCellsEvent as NLCE
from enums.entity_enums import EntityType as ET, EntityCategory as EC, InputEnums as IE, PowerUpStates as PUS
from state_machines.default_state_machine import DefaultStateMachine
from entity.controllers.skull_controller import SkullController
from entity.controllers.player_controller import PlayerController
from entity.controllers.knight_controller import KnightController
from entity.controllers.winged_knight_controller import WingedKnightController
from collisions.collision_manager import CollisionManager
from renderers.default_renderer import DefaultRenderer
from physics.ground_physics import GroundPhysics
from base_manager import BaseManager
from system.system_buses import entity_manager_bus
class EntityManager(BaseManager):
    def __init__(self, animation_manager=None, attack_manager=None, context=None):
        super().__init__(context=context)
        self.local_bus = entity_manager_bus(self)
        if not animation_manager:
            animation_manager = AnimationManager(context)
        if not attack_manager:
            attack_manager = AttackManager(context)
        self.controllers = {}
        # controllers are loaded depending on entity type, done when loading a level
        self.physics = {}
        # depends on entity type, what physics to apply. floating skulls don't fall...
        self.state_machines = {}
        # depends on entity type, different state machines for different entity types
        # but just using default for now
        self.state_machine = DefaultStateMachine(self.context.bus, self.local_bus)
        self.entities_setup = []
        # types of entities setup already

        self.animation_manager = animation_manager
        self.attack_manager = attack_manager
        self.context = context
        self.main_return_events = []
        self.main_return_commands = []
        self.renderer = DefaultRenderer()

        self.local_events = []
        self.local_commands = []
        self.state_change_events = []

    def setup_bus(self):
        self.context.bus.register_event_listener(NLCE, self)
        self.context.bus.register_command_listener(PhysicsCommand, self)


    def update_entity(self, entity):

        # new way to update entity:
        # self.entity_events, self.entity_commands,
        # controllers only get input events once, so they don't need to be called multiple times and can be outside of this, but things that have multiple events/commands get acces to a slot in slot out system
        # so, minibus will be intermediary for entity_manager to get events and commands from subsystems, rather than them posting directly
        # why? might refactor it to be more main bus like with setup minibus, where they chose what they listen to, but for now entity manager will decide who gets what events/commands, but doing it like this makes refactor very easy, as they'll just send it to send_event/send_command of the minibus, it'll redirect it to the local_event, local_command lists here
        # then entity manager will start a process loop, handling all events there until none are left
        # and the sub systems can add to the loop while it's going, why? because sometimes they need to interact back and forth
        # there will also be a state_change update, which happens after all events and commands are processed, so minibus will have a way to identify and pass those to entity manager too


        # input events are one shot, only come from controller, so it will be most decoupled. Just hand it context and entity, it returns input events
        input_events = []
        input_events = input_events + self.controllers[entity.entity_type].update(entity, self.context)
        events, commands = self.state_machine.input_events(entity, input_events)

        animation_event = self.animation_manager.update(entity)
        if animation_event:
            events.append(animation_event)

        killswitch = False
        count = 0

        while (events or commands) and not (killswitch):
            if events:
                new_events, new_commands = self.delegate_event(events.pop(0), entity)
                events.extend(new_events)
                commands.extend(new_commands)
            if commands:
                new_events, new_commands = self.delegate_command(commands.pop(0), entity)
                events.extend(new_events)
                commands.extend(new_commands)
            count += 1
            if count > 100:
                killswitch = True
                # just a killswitch to prevent infinite loops for now. shouldn't need it if designed well, but just in case.

        state_updates = self.physics[entity.entity_category].update(entity)
        # should just return events as of now
        attack_event = self.attack_manager.update(entity)

        # clean this up later, make it more readable and consider organizing based match events to be drawn from a module or such, but for now fine, maybe make main events not a class attribute later
        if attack_event:
            match attack_event:
                case AFE():
                    state_updates.append(attack_event)


        events, commands = self.state_machine.state_updates(entity, state_updates)
        if events or commands:
            for event in events:
                self.delegate_event(event, entity)
            for command in commands:
                self.delegate_command(command, entity)


    def process_loop(self):
        killswitch = False
        count = 0
        # shouldn't need killswitch, but have it just in case
        # raise error if it hits over 100, this is during testing and building
        while (self.local_events or self.local_commands):
            if self.local_events:
                event = self.local_events.pop(0)
                self.handle_event(event)
            if self.local_commands:
                command = self.local_commands.pop(0)
                self.handle_command(command)
            count += 1
            if count > 100:
                killswitch = True
                raise Exception("EntityManager process loop exceeded maximum iterations.")



        # expand to sound later

    def handle_event(self, event):
        # this is for when external systems want to pass events to entity manager to be delegated to respective systems
        match event:
            case PE():
                self.physics[event.entity.entity_category].handle_event(event)
            case NLCE():
                self.handle_newly_loaded_cells(event)


    def handle_command(self, command):
        # handle commands are for commands external systems have given to entity manager to be delegated to respective systems
        match command:
            case PhysicsCommand():
                self.physics[command.entity.entity_category].handle_command(command)

    def handle_newly_loaded_cells(self, event: NLCE):
        # when new cells are loaded, setup entities in those cells
        for cell in event.loaded_cells:
            self.setup_entities(cell.entity_types)
        return []

    def delegate_event(self, event, entity):
        # delegate is for its respective held systems
        match event:
            case StateChangedEvent():
                # only animation manager needs it for now, but later it might be useful to have it delegated to all other systems too
                self.animation_manager.handle_event(event, entity)


        return [], []  # Return empty lists if no new events/commands

    def delegate_command(self, command, entity):
        commands = []
        match command:
            case MovementCommand():
                return self.physics[entity.entity_category].handle_command(command, entity)
            case AttackCommand():
                return self.attack_manager.handle_command(command, entity)
            case EffectCommand():
                self.main_return_commands.append(command)
            case AudioCommand():
                self.main_return_commands.append(command)
        return [], commands  # Return empty lists if no new events/commands


    def draw(self, entity):
        self.renderer.render(entity)

    def setup_entity(self, entity_type):
        # sets up the controllers, physics, and state machines for the respective entity type
        # honestly as it gets more complex, i'll make a default physics module that has a basic set of physics
        # the thought will be so multiple entities can remake the sam
        match entity_type:
            # separate this out later when i have time to think of how to best structure accessing a myriad of different entity types, for now just import directly and use
            case ET.SKULL:
                # edit this so it only adds if doesn't exist
                self.setup_controller(ET.SKULL, SkullController)
                # for now, just default physics, not flying
                self.setup_physics(EC.GROUND, GroundPhysics, context=self.context)
                # just using default player physics for now
                # self.state_machines[] = SkullStateMachine()
                # just use a default state machine for now
            case ET.PLAYER:
                self.entities_setup.append(ET.PLAYER)
                # refactor later, but for now only player directly added through setup entity, others are from setup_entities
                self.setup_controller(ET.PLAYER, PlayerController)
                self.setup_physics(EC.GROUND, GroundPhysics, context=self.context)

            case ET.KNIGHT:
                self.setup_controller(ET.KNIGHT, KnightController)
                self.setup_physics(EC.GROUND, GroundPhysics, context=self.context)
            case ET.WINGED_KNIGHT:
                self.setup_controller(ET.WINGED_KNIGHT, WingedKnightController)
                self.setup_physics(EC.GROUND, GroundPhysics, context=self.context)
                # for now just use ground physics, revisit later to make a flying physics module


    def setup_entities(self, entity_types):
        for entity_type in entity_types:
            if entity_type not in self.entities_setup:
                self.setup_entity(entity_type)
                self.entities_setup.append(entity_type)

    def setup_physics(self, entity_category, physics_module, context=None):
        if not context:
            context = self.context
        if entity_category not in self.physics:
            self.physics[entity_category] = physics_module(context)

    def setup_controller(self, entity_type, controller):
        if entity_type not in self.controllers:
            self.controllers[entity_type] = controller()
