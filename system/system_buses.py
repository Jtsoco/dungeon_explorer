

from events_commands.events import Event
from events_commands.commands import Command, AudioCommand, EffectCommand, CollisionCommand, PhysicsCommand

class SystemBus:

    # it has events, and it allows entities to register themselves to listen for events and commands, which they hold onto until processed
    def __init__(self):
        #
        self.command_listeners = {
            AudioCommand: [],
            EffectCommand: [],
            CollisionCommand: [],
            PhysicsCommand: [],
        }
        #
        self.event_listeners = {}
        self.command_keys = set(self.command_listeners.keys())
    def register_new_event(self, event):
        pass

    def register_new_command(self, command):
        pass

    def register_event_listener(self, event_type, listener):
        pass

    def register_command_listener(self, command_type, listener):
        pass

    def get_command_key(self, command):
        # because some keys may be subclasses of others
        for key in self.command_keys:
            if isinstance(command, key):
                return key
        return None

    def get_event_key(self, event):
        pass

    def send_command(self, command):
        key = self.get_command_key(command)
        if key:
            listeners = self.command_listeners[key]
            for listener in listeners:
                # use notify command, to indicate that it's a command to be acted upon during update cycle
                listener.notify_command(command)
