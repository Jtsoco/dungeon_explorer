import pyxel
def display_info(string, pos_x=0, pos_y=0):
    """Display debug info on screen at specified position."""
    pyxel.text(pos_x, pos_y, f"DI: {string}", 7)
