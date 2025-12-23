from enums.entity_enums import InputEnums as IE, DirectionState as DS
# change InputEvents to InputEnums
from events_commands.events import InputEvent
import pyxel

class PlayerController():
    def __init__(self):
        self.recent_movement = []

    def poll_events(self):
        new_recents = []
        rl_movement = []
        events = []
        if pyxel.btn(pyxel.KEY_LEFT):
            rl_movement.append(InputEvent(IE.MOVE, direction=DS.LEFT))
        if pyxel.btn(pyxel.KEY_RIGHT):
            rl_movement.append(InputEvent(IE.MOVE, direction=DS.RIGHT))
        if pyxel.btn(pyxel.KEY_SPACE):
            new_recents.append(InputEvent(IE.JUMP))
        if pyxel.btn(pyxel.KEY_D):
            new_recents.append(InputEvent(IE.ATTACK))

        if not rl_movement or (len(rl_movement) == 2):
            new_recents.append(InputEvent(IE.STOP_MOVE))
        else:
            new_recents.extend(rl_movement)
        # this checks if there are any new events since last time
        # only turning new events into events to return
        events = [event for event in new_recents if event not in self.recent_movement]
        # then, take all the inputs and indicate it was pressed this frame
        self.recent_movement = new_recents
        return events

    def update(self, entity_data=None, context=None):
        # this is just for player, so entity data not needed for now, but to be compatible with other controllers needs to accept data and context
        input_events = self.poll_events()
        return input_events
