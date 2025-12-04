from player.player_enums import MovementState as MS
from events_commands.events import StateChangedEvent

class AnimationManager():
    def __init__(self):
        pass  # Placeholder for future implementation

    def update(self, data):
        current_frame = data.animation_data.last_frame
        # current_frame = self.get_frame(data)
        if self.next_frame(current_frame.duration, data.animation_data):
            current_frame = self.get_frame(data)
            # Frame advanced
            # if the state is an attack state, and next frame is true and current frame is 0, then signal that attack is done with a return statement sending attack finished event
            # however, it will also depend on the attack type whether it will end or loop, for example an air attack might continue till it hits the ground
            # focus on ground attacks for now
            pass
        data.animation_data.frame_timer += 1
        return None

    def handle_event(self, event, data):
        match event:
            case StateChangedEvent():
                self.reset(data)
                # set new animation based on new state
                # could also pass in the new state via the event for more flexibility
    # this will respond to a state change event and reset animation frame counter, and set new animation accordingly

    def next_frame(self, frame_duration, data):
        if data.frame_timer >= frame_duration:
            data.current_frame += 1
            data.frame_timer = 0
            return True
        return False

    def reset(self, player_data):
        data = player_data.animation_data
        last = data.last_frame
        data.last_frame = self.get_frame(player_data)
        if last != data.last_frame:
            # reset frame counter only if the animation actually changed
            data.current_frame = 0
            data.frame_timer = 0


    def get_frame(self, player_data):
        state = player_data.movement_state
        animations = player_data.animation_data.animations
        current_animation = animations.get(state, animations[MS.IDLE])
        # it should have a default idle animation no matter what
        frame_index = player_data.animation_data.current_frame = player_data.animation_data.current_frame % len(current_animation)
        return current_animation[frame_index]
