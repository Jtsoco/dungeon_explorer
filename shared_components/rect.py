class Rect:
    # this class is to hold physical dimensions for entities and such
    def __init__(self, w: int, h: int, position=(0,0)):
        self.width = w
        self.height = h
        self.position = position  # x, y tuple
    def is_rect_colliding(self, other_rect):
        # simple aabb collision detection
        if (self.position[0] < other_rect.position[0] + other_rect.width and
            self.position[0] + self.width > other_rect.position[0] and
            self.position[1] < other_rect.position[1] + other_rect.height and
            self.position[1] + self.height > other_rect.position[1]):
            return True
        return False

    def is_colliding(self, other_pos, other_w_h):
        # simple aabb collision detection
        if (self.position[0] < other_pos[0] + other_w_h[0] and
            self.position[0] + self.width > other_pos[0] and
            self.position[1] < other_pos[1] + other_w_h[1] and
            self.position[1] + self.height > other_pos[1]):
            return True
        return False
