
class AnimationFrame():
    def __init__(self, pos: tuple, duration: int=6, offset: tuple=(0,0), rotation = 0, w_h: tuple = (8,8), scale=1):
        self.pos = pos
        self.duration = duration
        self.offset = offset
        self.rotation = rotation
        self.w_h = w_h
        self.scale = scale

    def copy(self):
        return AnimationFrame(
            pos=self.pos,
            duration=self.duration,
            offset=(self.offset[0], self.offset[1]),
            rotation=self.rotation,
            w_h=(self.w_h[0], self.w_h[1]),
            scale=self.scale
        )
