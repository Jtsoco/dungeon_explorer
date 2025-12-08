from animations.animation_manager import AnimationManager
from attack.attack_manager import AttackManager
from events_commands.commands import MovementCommand, AttackCommand
from events_commands.events import StateChangedEvent
from enums.entity_enums import EntityType

class EntityManager():
    def __init__(self, animation_manager=AnimationManager(), attack_manager=AttackManager()):
        self.controllers = {}
        # controllers are loaded depending on entity type, done when loading a level
        self.physics = {}
        # depends on entity type, what physics to apply. floating skulls don't fall...
        self.state_machines = {}
        # depends on entity type, different state machines for different entity types

        self.animation_manager = animation_manager
        self.attack_manager = attack_manager


    def update(self, entity):
        events, commands = [], []

        input_events = []
        input_events = input_events + self.controllers[entity.entity_type].poll_events()

        animation_event = self.animation_manager.update(entity.data)
        if animation_event:
            input_events.append(animation_event)

        killswitch = False
        count = 0

        while (events or commands) and not (killswitch):
            if events:
                new_events, new_commands = self.delegate_event(events.pop(0))
                events.extend(new_events)
                commands.extend(new_commands)
            if commands:
                new_events, new_commands = self.delegate_command(commands.pop(0))
                events.extend(new_events)
                commands.extend(new_commands)
            count += 1
            if count > 100:
                killswitch = True
                # just a killswitch to prevent infinite loops for now. shouldn't need it if designed well, but just in case.

        state_updates = self.physics[entity.entity_type].update(entity)
        # should just return events as of now
        attack_event = self.attack_manager.update(entity)
        if attack_event:
            state_updates.append(attack_event)

        state_change = self.state_machines[entity.entity_type].state_updates(entity, state_updates)
        if state_change:
            self.delegate_event(state_change)

    def delegate_event(self, event, entity):
        match event:
            case StateChangedEvent():
                # only animation manager needs it for now, but later it might be useful to have it delegated to all other systems too
                self.animation_manager.handle_event(event, entity)
        return [], []  # Return empty lists if no new events/commands

    def delegate_command(self, command, entity):
        match command:
            case MovementCommand():
                return self.player_physics.handle_command(command, entity)
            case AttackCommand():
                return self.attack_manager.handle_command(command, entity)

    def draw(self, entity):
        self.renderer.render(entity)
