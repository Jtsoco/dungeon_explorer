from enums.entity_enums import InputEnums as IE, DirectionState as DS
# change InputEvents to InputEnums
from events_commands.events import InputEvent
import pyxel

class PlayerController():
    def __init__(self):
        self.recent_movement = set()

    def poll_events(self):
        print('recent movements before polling:', self.recent_movement)
        new_recents = set()
        rl_movement = set()
        events = []
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            rl_movement.add(InputEvent(IE.MOVE, direction=DS.LEFT))
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            rl_movement.add(InputEvent(IE.MOVE, direction=DS.RIGHT))
        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
            new_recents.add(InputEvent(IE.JUMP))
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            new_recents.add(InputEvent(IE.ATTACK))
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_X):
            new_recents.add(InputEvent(IE.BLOCK))
        else:
            new_recents.add(InputEvent(IE.STOP_BLOCK))


        # for now, polling for rl movement as a quick bug fix
        if not rl_movement or (len(rl_movement) == 2):
            new_recents.add(InputEvent(IE.STOP_MOVE))
        else:
            new_recents.update(rl_movement)
        # this checks if there are any new events since last time
        # only turning new events into events to return
        # events = [event for event in new_recents if event not in self.recent_movement]
        new_recent_movements = set()
        for event in new_recents:
            new_recent_movements.add((event.input_type, event.direction))
            if (event.input_type, event.direction) not in self.recent_movement:
                events.append(event)

        # print(f"New Input Events: {[str(event) for event in events]}")
        # then, take all the inputs and indicate it was pressed this frame
        self.recent_movement = new_recent_movements
        return events

    def update(self, entity_data=None, context=None):
        # this is just for player, so entity data not needed for now, but to be compatible with other controllers needs to accept data and context
        input_events = self.poll_events()
        return input_events
