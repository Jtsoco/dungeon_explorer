from enums.entity_enums import DirectionState as DS
import pyxel
def draw_weapon(entity_data, x, y, image_bank=0, color_key=2,):
    current_frame = entity_data.animation_data.get_current_frame()
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
    # weapon_hitbox_pos = entity_data.weapon.get_position(entity_data)

    # hitbox = entity_data.weapon.get_current_hitbox()
    # pyxel.rect(weapon_hitbox_pos[0], weapon_hitbox_pos[1], hitbox[0], hitbox[1], 8)


def draw_shield(entity_data, x, y, image_bank=0, color_key=2):
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

def draw_entity(entity_data, x, y, image_bank=0, color_key=2, additions=True):
    if additions:
        if entity_data.weapon:
            draw_weapon(entity_data, x, y, image_bank, color_key)
    current_frame = entity_data.animation_data.get_current_frame()
    u = current_frame.pos[0] * 8
    v = current_frame.pos[1] * 8
    # have to multiply by 8 because each 'tile' in the sprite sheet is 8x8 pixels
    width = current_frame.w_h[0]
    height = current_frame.w_h[1]
    rotation = current_frame.rotation
    # just a default because i'm only using this for now
    width = width if entity_data.direction_state == DS.RIGHT else -width

    # pyxel.rect(entity_data.position[0], entity_data.position[1], entity_data.w_h[0], entity_data.w_h[1], 8)
    pyxel.blt(x, y, image_bank, u, v, width, height, color_key, rotate=rotation)
    if additions:
        if entity_data.shield:
            draw_shield(entity_data, x, y, image_bank, color_key)
    # pyxel.rect(x, y, entity_data.rect.width, entity_data.rect.height, 6)

# TODO change these to allow scale to be easily modified later

def draw_only_weapon(weapon, x, y, image_bank=0, color_key=2, line=True, inventory=True):
    if inventory:
        weapon_frame = weapon.get_inventory_frame()
        w_width = 8
        w_height = 8
    else:
        weapon_frame = weapon.get_current_frame()
        w_width = weapon_frame.w_h[0]
        w_height= weapon_frame.w_h[1]
    if line:
        pyxel.line(x - 4, y + w_height, x + w_width - 4, y + w_height, 8)

    wu = weapon_frame.pos[0] * 8
    wv = weapon_frame.pos[1] * 8
    pyxel.blt(x, y, image_bank, wu, wv, w_width, w_height, color_key, rotate=weapon_frame.rotation)

def draw_square(x, y, width, height, color=8):
    pyxel.rectb(x, y, width, height, color)

def draw_only_shield(shield, x, y, image_bank=0, color_key=2, line=True):
    shield_frame = shield.get_current_frame()
    s_width = shield_frame.w_h[0]
    s_height = shield_frame.w_h[1]
    wu = shield_frame.pos[0] * 8
    wv = shield_frame.pos[1] * 8
    if line:
        pyxel.line(x - 4, y + s_height, x + s_width, y + s_height, 8)
    pyxel.blt(x, y, image_bank, wu, wv, s_width, s_height, color_key, rotate=shield_frame.rotation)
