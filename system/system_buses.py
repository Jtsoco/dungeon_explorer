

from events_commands.events import Event, DeathEvent, BoundaryCollisionEvent, NewlyLoadedCellsEvent, PlayerEvent, BossDeathEvent, StateChangedEvent, MovementEvent, AttackFinishedEvent
from events_commands.commands import Command, AudioCommand, EffectCommand, CollisionCommand, PhysicsCommand, DamageCommand, HUDCommand

class SystemBus:

    # it has events, and it allows entities to register themselves to listen for events and commands, which they hold onto until processed
    def __init__(self):
        #
        self.command_listeners = {
            AudioCommand: [],
            EffectCommand: [],
            CollisionCommand: [],
            PhysicsCommand: [],
            DamageCommand: [],
            HUDCommand: [],
        }
        #
        self.event_listeners = {
            DeathEvent: [],
            BoundaryCollisionEvent: [],
            NewlyLoadedCellsEvent: [],
            PlayerEvent: [],
            BossDeathEvent: [],

        }


    def register_new_event(self, event):
        pass

    def register_new_command(self, command):
        pass

    def register_event_listener(self, event_type, listener):
        self.event_listeners[event_type].append(listener)

    def register_command_listener(self, command_type, listener):
        self.command_listeners[command_type].append(listener)

    def get_command_key(self, command):
        # because some keys may be subclasses of others
        command_type = type(command)
        if command_type in self.command_listeners:
            return command_type
        for key in self.command_listeners.keys():
            if isinstance(command, key):
                return key
        return None

    def get_event_key(self, event):
        # check for exact match first
        event_type = type(event)
        if event_type in self.event_listeners:
            return event_type

        # else see if it's a subclass some keys may be subclasses of others

        for key in self.event_listeners.keys():
            if isinstance(event, key):
                return key
        return None

    def send_command(self, command):

        key = self.get_command_key(command)
        if key:
            listeners = self.command_listeners[key]
            for listener in listeners:
                # use notify command, to indicate that it's a command to be acted upon during update cycle
                listener.notify_command(command)

    def send_event(self, event):
        key = self.get_event_key(event)
        if key:
            listeners = self.event_listeners[key]
            for listener in listeners:
                # use notify event, to indicate that it's an event to be acted upon during update cycle
                listener.notify_event(event)

class EntityManagerBus(SystemBus):
    # those who hold this know it as a local bus
    # this bus is for handling communication within subsystems, like the entity_manager handling its own events and commands internally in its
    # for now it just passes it directly to its receiver
    def __init__(self, receiver):
        self.receiver = receiver

    def send_command(self, command):
        self.receiver.local_commands.append(command)

    def send_event(self, event):
        match event:
            case StateChangedEvent():
                self.receiver.state_change_events.append(event)
            case MovementEvent() | AttackFinishedEvent():
                # movement events go to state updates for processing, as they are events that occur that may change state
                # if similar events that need to be processed for possible state updates arise, then maybe make a state update event parent class
                self.receiver.state_updates.append(event)
            case _:
                self.receiver.local_events.append(event)
