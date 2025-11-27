from player_enums import InputEnums as IE, DirectionState as DS
# change InputEvents to InputEnums
from ..events_commands.events import InputEvent
import pyxel

class PlayerController():
    def __init__(self):
        pass

    def poll_events(self):
        rl_movement = []
        events = []
        if pyxel.btn(pyxel.KEY_LEFT):
            rl_movement.append(InputEvent(IE.MOVE, direction=DS.LEFT))
        if pyxel.btn(pyxel.KEY_RIGHT):
            rl_movement.append(InputEvent(IE.MOVE, direction=DS.RIGHT))
        if pyxel.btn(pyxel.KEY_SPACE):
            events.append(InputEvent(IE.JUMP))

        if not rl_movement or (len(rl_movement) == 2):
            events.append(InputEvent(IE.STOP_MOVE))
        else:
            events.extend(rl_movement)
        return events
