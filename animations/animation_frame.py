class AnimationFrame():
    def __init__(self, pos: tuple, duration: int=6, offset: tuple=(0,0), rotation = 0, w_h: tuple = (8,8)):
        self.pos = pos
        self.duration = duration
        self.offset = offset
        self.rotation = rotation
        self.w_h = w_h
