from animations.animation_manager import AnimationManager
from attack.attack_manager import AttackManager
from events_commands.commands import MovementCommand, AttackCommand, EffectCommand, SoundCommand, AudioCommand, PhysicsCommand, DefenseCommand, BreakShieldCommand, BreakBlockCommand
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
from system.system_buses import EntityManagerBus
from defense.defense_manager import DefenseManager

class EntityManager(BaseManager):
    def __init__(self, animation_manager=None, attack_manager=None, context=None):
        super().__init__(context=context)
        self.local_bus = EntityManagerBus(self)
        if not animation_manager:
            animation_manager = AnimationManager(context)
        if not attack_manager:
            attack_manager = AttackManager(context, self.local_bus)

        self.defense_manager = DefenseManager(context, self.local_bus)

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
        self.state_updates = []

    def setup_bus(self):
        self.context.bus.register_event_listener(NLCE, self)
        self.context.bus.register_command_listener(PhysicsCommand, self)
        self.context.bus.register_command_listener(DefenseCommand, self)

    def reset_local(self):
        self.local_events = []
        self.local_commands = []
        self.state_change_events = []
        self.state_updates = []

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
        self.reset_local()

        input_events = []
        input_events = input_events + self.controllers[entity.entity_type].update(entity, self.context)
        self.state_machine.input_events(entity, input_events)
        self.animation_manager.update(entity)
        # actual flow as of now:
        # get inputs from controller
        # pass state machine, it adds commands/events as needed
        # update animation manager
        # process commands in a loop, as of now only 1 or 2 exist at a time, but could be more complex later, often it's just movement commmands being relayed to physics, which sets momentum and such, and it itself sending state updates to queue state machine will use
        # basically state machine says set based on these movements states these momentums etc,
        # physics sets them
        # then update physics, moving entity based on its current state and velocities and such, previously set by physics in process loop,
        # then update attack manager, send any events needed or state updates
        # as of now, it doesn't send any other commands/events, so a second process loop isn't needed after this, but if it did, would do so here
        # then take state updates, pass them to state machine, it handles state
        # if any state change occurred, then inform whoever needs to konw
        # delegate events only has state change event in it for now, so this is fine to use delegate event rather than state change handle method,
        # then loop is done

        self.process_loop(entity)
                # just a killswitch to prevent infinite loops for now. shouldn't need it if designed well, but just in case.

        self.physics[entity.entity_category].update(entity)
        # should just return events as of now
        self.attack_manager.update(entity)
        self.defense_manager.update(entity)

        self.handle_state_updates(entity)



    def handle_state_updates(self, entity):
        self.state_machine.state_updates(entity, self.state_updates)
        if self.state_change_events:
            for event in self.state_change_events:
                    self.delegate_event(event, entity)

    def process_loop(self, entity):
        killswitch = False
        count = 0
        # shouldn't need killswitch, but have it just in case
        # raise error if it hits over 100, this is during testing and building
        while (self.local_events or self.local_commands):
            if self.local_events:
                event = self.local_events.pop(0)
                # delegate for local events, handle is for events received by external systems
                self.delegate_event(event, entity)
            if self.local_commands:
                command = self.local_commands.pop(0)
                self.delegate_command(command, entity)
            count += 1
            if count > 100:
                killswitch = True
                self.reset_local()
                raise Exception("Entity Manager Process Loop Killswitch Activated - Possible Infinite Loop Detected")



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
            case BreakShieldCommand():
                self.break_shield_command(command)



    def handle_newly_loaded_cells(self, event: NLCE):
        # when new cells are loaded, setup entities in those cells
        for cell in event.loaded_cells:
            self.setup_entities(cell.entity_types)

    def delegate_event(self, event, entity):
        # delegate is for its respective held systems
        match event:
            case StateChangedEvent():
                # only animation manager needs it for now, but later it might be useful to have it delegated to all other systems too
                self.animation_manager.handle_event(event, entity)



    def delegate_command(self, command, entity):
        match command:
            case MovementCommand():
                self.physics[entity.entity_category].handle_command(command, entity)
            case AttackCommand():
                self.attack_manager.handle_command(command, entity)
            case DefenseCommand():
                self.defense_manager.handle_command(command, entity)



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
            case ET.DARK_LORD:
                # for now, just this is fine
                self.setup_controller(ET.DARK_LORD, KnightController)
                self.setup_physics(EC.GROUND, GroundPhysics, context=self.context)


    def setup_entities(self, entity_types):
        for entity_type in entity_types:
            if entity_type not in self.entities_setup:
                self.setup_entity(entity_type)
                self.entities_setup.append(entity_type)

    def setup_physics(self, entity_category, physics_module, context=None):
        if not context:
            context = self.context
        if entity_category not in self.physics:
            self.physics[entity_category] = physics_module(context, self.local_bus)

    def setup_controller(self, entity_type, controller):
        if entity_type not in self.controllers:
            self.controllers[entity_type] = controller()

    def break_shield_command(self, command):
        # gets its own method because may involve state machine and defense manager
        entity_data = command.target
        self.defense_manager.handle_command(command, entity_data)
        # may have state updates afterwards to process
        self.handle_state_updates(entity_data)
