from player_controller import PlayerController
from player_data import PlayerData
from player_renderer import PlayerRenderer
from player_state_machine import PlayerStateMachine as StateMachine

class PlayerEntity:
    def __init__(self):
        self.events = []
        self.commands = []
        self.controller = PlayerController()
        self.data = PlayerData()
        self.renderer = PlayerRenderer()
        self.state_machine = StateMachine()


    def update(self):
        # get events from controller
        # save to input qeue
        # pass with data to state machine
        # get commands/events from state machine
        # get regular commands/events from state machine update after passing it data
        # while events and commands in respective qeues, pass to relevant systems, eg physics, get any response events, and continue loop until both queues are empty
        pass

    def draw(self):
        pass
