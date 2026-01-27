class AppController():

    def __init__(self, bus):
        self.bus = bus
        self.recent_keys = set()
        # this prevents double processing and long button holds from doing things multiple times


    def notify_command(self, command):
        pass

    def update(self):
        # it takes any new input commands, makes sure there wasn't a repeat from last frame, then sends them
        # basically it holds onto a command until the respective button creating it is no longer pressed
        new_recents = set()
        new_recents.update(self.handle_inputs())
        new_keys = new_recents - self.recent_keys
        commands_to_send = self.process_keys(new_keys)

        for command in commands_to_send:
            self.send_command(command)

        self.recent_keys = new_recents

    def process_keys(self, new_recents):
        return set()

    def handle_inputs(self):
        # return a set of recent commands
        recents = set()
        return recents

    def send_command(self, command):
        # meant to be overwritten in subclasses, where they handle what command will be sent

        pass
