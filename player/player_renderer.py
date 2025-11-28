import pyxel

class PlayerRenderer():
    def __init__(self):
        pass
    # give each entity a frame counter/animation class that keeps track of states animation frames

    def render(self, player_data):
        pyxel.rect(player_data.position[0], player_data.position[1], player_data.w_h[0], player_data.w_h[1], 8)
    # note, need to decide who handles what costume is active, the data or the renderer, need to properly decide purpose of this class

# for now, just start drawing a player rectangle at player position
