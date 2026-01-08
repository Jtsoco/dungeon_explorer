class Effect:
    # a class for scene effects, like little animations for deaths and such
    def __init__(self, effect_type, position, animation_frames):
        self.effect_type = effect_type
        self.position = position
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.finished = False
        self.frame_timer = 0

    def update(self):
        pass

    def get_current_animation_frame(self):
        # to improve readability this method grabs not the current frame index but the actual frame data
        return self.animation_frames[self.current_frame]

    # base on animation_manager methods, probably consolidate things into a module later
