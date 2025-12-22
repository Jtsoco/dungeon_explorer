class AnimationFrame():
    def __init__(self, pos: tuple, duration: int=6, offset: tuple=(0,0)):
        self.pos = pos
        self.duration = duration
        self.offset = offset
