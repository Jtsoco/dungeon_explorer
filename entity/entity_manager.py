from animations.animation_manager import AnimationManager
from attack.attack_manager import AttackManager
from events_commands.commands import MovementCommand, AttackCommand
from events_commands.events import StateChangedEvent
from enums.entity_enums import EntityType as ET, EntityCategory as EC
from player.player_state_machine import PlayerStateMachine
from player.player_physics import PlayerPhysics
from entity.controllers.skull_controller import SkullController

class EntityManager():
    def __init__(self, animation_manager=AnimationManager(), attack_manager=AttackManager(), context=None):
        self.controllers = {}
        # controllers are loaded depending on entity type, done when loading a level
        self.physics = {}
        # depends on entity type, what physics to apply. floating skulls don't fall...
        self.state_machines = {}
        # depends on entity type, different state machines for different entity types
        # but just using default for now
        self.state_machine = PlayerStateMachine()
        self.entities_setup = []
        # types of entities setup already

        self.animation_manager = animation_manager
        self.attack_manager = attack_manager
        self.context = context



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
        if attack_event:
            state_updates.append(attack_event)

        state_change = self.state_machine.state_updates(entity, state_updates)
        if state_change:
            self.delegate_event(state_change, entity)

    def delegate_event(self, event, entity):
        match event:
            case StateChangedEvent():
                # only animation manager needs it for now, but later it might be useful to have it delegated to all other systems too
                self.animation_manager.handle_event(event, entity)
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
                self.controllers[ET.SKULL] = SkullController()
                # for now, just default physics, not flying
                self.physics[EC.GROUND] = PlayerPhysics(self.context)
                # just using default player physics for now
                # self.state_machines[] = SkullStateMachine()
                # just use a default state machine for now

    def setup_entities(self, entity_types):
        for entity_type in entity_types:
            if entity_type not in self.entities_setup:
                self.setup_entity(entity_type)
                self.entities_setup.append(entity_type)
