import pyxel
from player.player_enums import MovementState as MS, DirectionState as DS, ActionState as AS

class PlayerRenderer():
    def __init__(self):
        pass
        # this will have lists in it for each costume type
    # give each entity a frame counter/animation class that keeps track of states animation frames


    def render(self, player_data, color_key=2):
        width = 8  # hardcoded for now, as its a frame width of 8 in the sprite sheet, revisit later
        height = 8  # hardcoded for now, as its a frame height of 8 in the sprite sheet, revisit later
        x = player_data.position[0]
        y = player_data.position[1]

        current_frame = player_data.animation_data.get_current_frame()
        u = current_frame.pos[0] * 8
        v = current_frame.pos[1] * 8
        # have to multiply by 8 because each 'tile' in the sprite sheet is 8x8 pixels
        image_bank = 0
        # just a default because i'm only using this for now
        width = width if player_data.direction_state == DS.RIGHT else -width

        pyxel.blt(x, y, image_bank, u, v, width, height, color_key)
        # pyxel.rect(player_data.position[0], player_data.position[1], player_data.w_h[0], player_data.w_h[1], 8)
        if player_data.weapon:
            weapon_frame = player_data.weapon.get_current_frame()
            wu = weapon_frame.pos[0] * 8
            wv = weapon_frame.pos[1] * 8
            w_width = 8 if player_data.direction_state == DS.RIGHT else -8
            # for now just hardcoding weapon width and height, revisit later
            pyxel.blt(x, y, image_bank, wu, wv, w_width, 8, color_key)



        # blt(x,y,img,u,v,w,h,colkey)
    # note, need to decide who handles what costume is active, the data or the renderer, need to properly decide purpose of this class

# for now, just start drawing a player rectangle at player position
