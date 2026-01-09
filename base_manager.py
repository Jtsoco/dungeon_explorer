class BaseManager():
    def __init__(self, context):
        self.context = context
        self.setup_bus()

        self.queued_events = []
        self.queued_commands = []

    def setup_bus(self):
        pass

    def notify_command(self, command):
        self.queued_commands.append(command)

    def notify_event(self, event):
        self.queued_events.append(event)

    def update(self):
        # just need to interact with this from outside to process queued events and commands,
        # and activate main update loop,
        # so instead of changing update just change the three methods called here
        for command in self.queued_commands:
            self.handle_command(command)
        self.queued_commands.clear()
        for event in self.queued_events:
            self.handle_event(event)
        self.queued_events.clear()
        self.handle_updates()

    def handle_event(self, event):
        pass

    def handle_command(self, command):
        pass
# handle event and command are now to be defined as how the manager sorts through them in their update loop

    def handle_updates(self):
        pass
    # here is where the main logic of their update loop will go
