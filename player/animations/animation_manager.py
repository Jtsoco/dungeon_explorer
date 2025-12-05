from player.player_enums import MovementState as MS
from events_commands.events import StateChangedEvent

class AnimationManager():
    def __init__(self):
        pass  # Placeholder for future implementation

    def update(self, data):
        current_frame = data.animation_data.get_current_frame()
        # current_frame = self.get_frame(data)
        if self.next_frame(current_frame.duration, data.animation_data):
            pass
            # Frame advanced
            # if the state is an attack state, and next frame is true and current frame is 0, then signal that attack is done with a return statement sending attack finished event
            # however, it will also depend on the attack type whether it will end or loop, for example an air attack might continue till it hits the ground
            # focus on ground attacks for now
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
        # just the logic to handle upping the current frame based on duration
        if data.frame_timer >= frame_duration:
            data.current_frame += 1
            data.frame_timer = 0
            self.check_current_frame_index(data)
            return True
        return False

    def check_current_frame_index(self, data):
        data.current_frame %= len(data.current_animation)

    def set_next_animation(self, animation_data, animation):
        animation_data.current_animation = animation

    def get_next_animation(self, player_data):
        return player_data.animation_data.animations.get(player_data.movement_state, player_data.animation_data.animations[MS.IDLE])

    def reset(self, player_data):
        data = player_data.animation_data
        old_animation = data.current_animation
        new = self.get_next_animation(player_data)
        if new != old_animation:
            # reset frame counter only if the animation actually changed

            data.current_frame = 0
            data.frame_timer = 0
            self.set_next_animation(data, new)


    def get_frame(self, player_data):
        frame = player_data.animation_data.get_current_frame()

        return frame
