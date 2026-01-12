from shared_components.rect import Rect
class Boundary:
    def __init__(self, boundary_type, position, w_h = (8, 8)):
        self.boundary_type = boundary_type
        self.position = position  # position is a tuple (x, y)
        self.w_h = w_h
        self.rect = Rect(w_h[0], w_h[1], position)
