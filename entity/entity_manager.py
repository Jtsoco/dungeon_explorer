from animations.animation_manager import AnimationManager
from attack.attack_manager import AttackManager
from events_commands.commands import MovementCommand, AttackCommand
from events_commands.events import StateChangedEvent, PossibleCollisionEvent as PCE, AttackFinishedEvent as AFE, PhysicsEvent as PE
from enums.entity_enums import EntityType as ET, EntityCategory as EC
from state_machines.default_state_machine import DefaultStateMachine
from entity.controllers.skull_controller import SkullController
from entity.controllers.player_controller import PlayerController
from collisions.collision_manager import CollisionManager
from renderers.default_renderer import DefaultRenderer
from physics.ground_physics import GroundPhysics
class EntityManager():
    def __init__(self, animation_manager=AnimationManager(), attack_manager=AttackManager(), context=None):
        self.controllers = {}
        # controllers are loaded depending on entity type, done when loading a level
        self.physics = {}
        # depends on entity type, what physics to apply. floating skulls don't fall...
        self.state_machines = {}
        # depends on entity type, different state machines for different entity types
        # but just using default for now
        self.state_machine = DefaultStateMachine()
        self.entities_setup = []
        # types of entities setup already

        self.animation_manager = animation_manager
        self.attack_manager = attack_manager
        self.context = context
        self.main_return_events = []
        self.renderer = DefaultRenderer()



    def update(self, entity):
        events, commands = [], []

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
                case PCE():
                    # collision events are main events
                    # consider dividing events into main and sub, or lvl1 lvl2 event types later to inherit from for easier filtering
                    self.main_return_events.append(attack_event)

        state_change = self.state_machine.state_updates(entity, state_updates)
        if state_change:
            self.delegate_event(state_change, entity)

        events = self.main_return_events.copy()
        self.main_return_events.clear()

        # expand to sound later
        return events

    def handle_event(self, event):
        # this is for when external systems want to pass events to entity manager to be delegated to respective systems
        match event:
            case PE():
                self.physics[event.entity.entity_category].handle_event(event)
        return []


    def delegate_event(self, event, entity):
        match event:
            case StateChangedEvent():
                # only animation manager needs it for now, but later it might be useful to have it delegated to all other systems too
                self.animation_manager.handle_event(event, entity)
            case PCE():
                self.main_return_events.append(event)

        return [], []  # Return empty lists if no new events/commands

    def delegate_command(self, command, entity):
        match command:
            case MovementCommand():
                return self.physics[entity.entity_category].handle_command(command, entity)
            case AttackCommand():
                return self.attack_manager.handle_command(command, entity)


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


    def setup_entities(self, entity_types):
        for entity_type in entity_types:
            if entity_type not in self.entities_setup:
                self.setup_entity(entity_type)
                self.entities_setup.append(entity_type)

    def setup_physics(self, entity_category, physics_module, context=None):
        if not context:
            context = self.context
        if not entity_category in self.physics:
            self.physics[entity_category] = physics_module(context)

    def setup_controller(self, entity_type, controller):
        if not entity_type in self.controllers:
            self.controllers[entity_type] = controller()
