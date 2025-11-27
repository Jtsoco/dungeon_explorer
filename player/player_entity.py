from player_controller import PlayerController
from player_data import PlayerData
from player_renderer import PlayerRenderer
from player_state_machine import PlayerStateMachine as StateMachine
from player_physics import PlayerPhysics

class PlayerEntity:
    def __init__(self):
        self.events = []
        self.commands = []
        self.controller = PlayerController()
        self.data = PlayerData()
        self.renderer = PlayerRenderer()
        self.state_machine = StateMachine()
        self.player_physics = PlayerPhysics()


    def update(self):
        events, commands = [], []
        input_events = []
        input_events = input_events + self.controller.poll_events()
        self.events, self.commands = self.state_machine.input_events(self.data, input_events)
        killswitch = False
        count = 0
        # returns a tuple of (events, commands)
        # might not need this while loop, might become a one shot process each frame
        while (events or commands) and not (killswitch):
            if events:
                new_events, new_commands = self.delegate_event(self.events.pop(0))
                events.extend(new_events)
                commands.extend(new_commands)
            if commands:
                new_events, new_commands = self.delegate_command(self.commands.pop(0))
                events.extend(new_events)
                commands.extend(new_commands)
            count += 1
            if count > 100:
                killswitch = True
                # just a killswitch to prevent infinite loops for now. shouldn't need it if designed well, but just in case.

        state_updates = self.player_physics.update(self.data)
        # update physics after all events and commands have been processed
        # state_updates can be events or commands to process after physics update
        # just keeping it events for now
        self.state_machine.input_events(self.data, state_updates)



    def delegate_event(self, event):
        pass

    def delegate_command(self, command):
        pass

    def draw(self):
        pass
