class AppController():

    def __init__(self, bus):
        self.bus = bus
        self.recent_commands = set()
        # this prevents double processing and long button holds from doing things multiple times


    def notify_command(self, command):
        pass

    def update(self):
        # it takes any new input commands, makes sure there wasn't a repeat from last frame, then sends them
        # basically it holds onto a command until the respective button creating it is no longer pressed
        new_recents = set()
        new_recents.update(self.handle_inputs())
        new_commands_to_send = new_recents - self.recent_commands
        for command in new_commands_to_send:
            self.bus.send_command(command)
        self.recent_commands = new_recents

    def handle_inputs(self):
        # return a set of recent commands
        recents = set()
        return recents
