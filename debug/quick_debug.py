import pyxel


def calculate_fps(previous_time, current_time, previous_frame_count, current_frame_count):
    """Calculate frames per second (FPS)."""
    time_diff = (current_time - previous_time).total_seconds()
    frame_diff = current_frame_count - previous_frame_count
    if time_diff > 0:
        fps = frame_diff / time_diff
    else:
        fps = 0
    # round fps and return
    return round(fps)




def display_info(string, pos_x=0, pos_y=0, cell_top_left = False):
    """Display debug info on screen at specified position."""
    if cell_top_left:
        cell_coor = get_cell_coordinates(pos_x, pos_y)
        pos_x = cell_coor[0] * 8 * 16
        pos_y = cell_coor[1] * 8 * 16

    pyxel.text(pos_x, pos_y, f"DI: {string}", 7)

def quick_point(x, y, color=7):
    """Draw a quick debug point on the screen."""
    pyxel.pset(x, y, color)

def get_cell_coordinates(x, y):
    """Convert pixel coordinates to cell coordinates."""
    CELL_SIZE = 16  # assuming each cell is 16x16 pixels
    cell_x = x // CELL_SIZE // 8
    cell_y = y // CELL_SIZE // 8
    return (cell_x, cell_y)
def get_brick_coordinates(x, y):
    """Convert pixel coordinates to brick (tile) coordinates."""
    BRICK_SIZE = 8  # assuming each brick is 8x8 pixels
    brick_x = x // BRICK_SIZE
    brick_y = y // BRICK_SIZE
    return (brick_x, brick_y)

def outline_rect(x, y, w, h, color=7):
    """Draw an outlined rectangle for debugging purposes."""
    pyxel.rect(x, y, w, 1, color)          # Top edge
    pyxel.rect(x, y + h - 1, w, 1, color)  # Bottom edge
    pyxel.rect(x, y, 1, h, color)          # Left edge
    pyxel.rect(x + w - 1, y, 1, h, color)  # Right edge

def outline_entity(entity_data, color=7):
    """Outline an entity's bounding box for debugging."""
    x, y = entity_data.position
    w, h = entity_data.w_h
    outline_rect(x, y, w, h, color)
