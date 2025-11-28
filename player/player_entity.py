from player.player_controller import PlayerController
from player.player_data import PlayerData
from player.player_renderer import PlayerRenderer
from player.player_state_machine import PlayerStateMachine as StateMachine
from player.player_physics import PlayerPhysics
from events_commands.commands import MovementCommand
class PlayerEntity:
    def __init__(self, context=None):
        self.events = []
        self.commands = []
        self.controller = PlayerController()
        self.data = PlayerData()
        self.renderer = PlayerRenderer()
        self.state_machine = StateMachine()
        self.player_physics = PlayerPhysics(context)
        self.tile_context = None
        # later will grab surrounding tiles and pass for collision detection to physics
        # it will just grab the most relevant tiles based on position
        # and store them until requested again
        self.context = context
        if self.context:
            x, y = self.context.player_start
            self.data.position = [x * self.context.BRICK_SIZE, y * self.context.BRICK_SIZE]


    def update(self):
        events, commands = [], []
        input_events = []
        input_events = input_events + self.controller.poll_events()
        events, commands = self.state_machine.input_events(self.data, input_events)
        killswitch = False
        count = 0
        # returns a tuple of (events, commands)
        # might not need this while loop, might become a one shot process each frame
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

        state_updates = self.player_physics.update(self.data)
        # should just return events as of now


        # update physics after all events and commands have been processed
        # state_updates can be events or commands to process after physics update
        # just keeping it events for now
        self.state_machine.state_updates(self.data, state_updates)



    def delegate_event(self, event):
        pass

    def delegate_command(self, command):
        match command:
            case MovementCommand():
                return self.player_physics.handle_command(command, self.data)

    def draw(self):
        self.renderer.render(self.data)
