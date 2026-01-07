class BaseManager():
    def __init__(self, context):
        self.context = context
        self.setup_bus()

        self.queued_events = []
        self.queued_commands = []

    def setup_bus(self):
        pass

    def notify_command(self, command):
        pass

    def notify_event(self, event):
        pass

    def update(self):
        pass
