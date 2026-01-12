import pyxel
from enums.entity_enums import MovementState as MS, DirectionState as DS
from debug.quick_debug import display_info
class DefaultRenderer():
    def __init__(self):
        pass
        # this will have lists in it for each costume type
    # give each entity a frame counter/animation class that keeps track of states animation frames


    def render(self, entity_data, color_key=2):
        """
        Renders an entity, and if they have a weapon that weapon too, using the weapons offset and the entity offset. Entity offset determines where they hold the weapon, weapon offset determines where the weapon handle is relative to upperleft of a frame
        """

        x = entity_data.rect.position[0]
        y = entity_data.rect.position[1]
        # float positions for y mean sometimes it's in the floor, using int here would make movement more jittery, so physics just requires it to be int for y positions, x doesn't have this limition and just uses floats, as no one cares if it goes in the wall a little

        current_frame = entity_data.animation_data.get_current_frame()
        u = current_frame.pos[0] * 8
        v = current_frame.pos[1] * 8
        # have to multiply by 8 because each 'tile' in the sprite sheet is 8x8 pixels
        width = current_frame.w_h[0]
        height = current_frame.w_h[1]
        rotation = current_frame.rotation
        image_bank = 0
        # just a default because i'm only using this for now
        width = width if entity_data.direction_state == DS.RIGHT else -width

        # pyxel.rect(entity_data.position[0], entity_data.position[1], entity_data.w_h[0], entity_data.w_h[1], 8)
        pyxel.blt(x, y, image_bank, u, v, width, height, color_key, rotate=rotation)
        if entity_data.weapon:
            weapon_frame = entity_data.weapon.get_current_frame()
            w_width = weapon_frame.w_h[0]
            w_height= weapon_frame.w_h[1]
            weapon_x = x
            weapon_y = y
            if entity_data.direction_state == DS.RIGHT:
                x_offset = abs(current_frame.offset[0] - weapon_frame.offset[0])
                weapon_x += x_offset

                # weapon_x = x
                y_offset = abs(current_frame.offset[1] - weapon_frame.offset[1])
                weapon_y -= y_offset
            else:
                x_offset = abs(current_frame.offset[0] - weapon_frame.offset[0])
                weapon_x = x - x_offset
                y_offset = abs(current_frame.offset[1] - weapon_frame.offset[1])
                weapon_y -= y_offset
                w_width = -w_width
            # display_info(f"X offset: {x_offset}", pos_x=x, pos_y=y-40)

            wu = weapon_frame.pos[0] * 8
            wv = weapon_frame.pos[1] * 8
            # for now just hardcoding weapon width and w_height, revisit later
            pyxel.blt(weapon_x, weapon_y, image_bank, wu, wv, w_width, w_height, color_key, rotate=weapon_frame.rotation)

        if entity_data.shield:
            shield_frame = entity_data.shield.get_current_frame()
            s_width = shield_frame.w_h[0]
            s_height = shield_frame.w_h[1]
            shield_x = x
            shield_y = y
            # shield doesn't use offset for now
            wu = shield_frame.pos[0] * 8
            wv = shield_frame.pos[1] * 8
            if entity_data.direction_state == DS.LEFT:
                s_width = -s_width
            pyxel.blt(shield_x, shield_y, image_bank, wu, wv, s_width, s_height, color_key, rotate=shield_frame.rotation)
            # shields don't rotate for now but might later




        # blt(x,y,img,u,v,w,h,colkey)
    # note, need to decide who handles what costume is active, the data or the renderer, need to properly decide purpose of this class

# for now, just start drawing a player rectangle at player position
