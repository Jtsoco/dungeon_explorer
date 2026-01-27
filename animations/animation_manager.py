from enums.entity_enums import MovementState as MS, ActionState as AS
from events_commands.events import StateChangedEvent
from base_manager import BaseManager
class AnimationManager(BaseManager):
    def __init__(self, context):
        super().__init__(context)
        pass  # Placeholder for future implementation

    def update(self, data):
        current_frame = data.animation_data.get_current_frame()
        # current_frame = self.get_frame(data)
        if self.next_frame(current_frame.duration, data.animation_data):
            pass
            # Frame advanced
            # so maybe some states will continue until animation ends, movement wise or so, but not implemented yet
            # however, it will also depend on the attack type whether it will end or loop, for example an air attack might continue till it hits the ground
            # focus on ground attacks for now
        data.animation_data.frame_timer += 1

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
            self.set_current_frame_index(data)
            return True
        return False

    def set_current_frame_index(self, data):
        data.current_frame %= len(data.current_animation)

    def set_next_animation(self, animation_data, animation):
        animation_data.current_animation = animation

    def get_next_animation(self, player_data):
        if player_data.action_state == AS.ATTACKING:
            return player_data.animation_data.animations.get(AS.ATTACKING, player_data.animation_data.animations[MS.IDLE])
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
