



class SystemBus:

    # it has events, and it allows entities to register themselves to listen for events and commands, which they hold onto until processed
    def __init__(self):
        #
        self.command_listeners = {}
        #
        self.event_listeners = {}

    def register_new_event(self, event):
        pass

    def register_new_command(self, command):
        pass

    def register_event_listener(self, event_type, listener):
        pass

    def register_command_listener(self, command_type, listener):
        pass
