import pyxel
from enums.entity_enums import MovementState as MS, DirectionState as DS
from debug.quick_debug import display_info
from HUD.player_draw import draw_entity
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

        image_bank = 0
        draw_entity(entity_data, x, y, image_bank, color_key, additions=True)

        # pyxel.rect(entity_data.position[0], entity_data.position[1], entity_data.w_h[0], entity_data.w_h[1], 8)


            # display_info(f"X offset: {x_offset}", pos_x=x, pos_y=y-40)



            # shields don't rotate for now but might later




        # blt(x,y,img,u,v,w,h,colkey)
    # note, need to decide who handles what costume is active, the data or the renderer, need to properly decide purpose of this class

# for now, just start drawing a player rectangle at player position
