import pyxel
from HUD.player_draw import draw_entity, draw_weapon, draw_shield
from app_level.app_enums import MenuState
class MenuRenderer():

    def __init__(self):
        pass

    def render(self, menu_data, game=None):
        if menu_data.menu_type == MenuState.PAUSE_MENU and game:
            self.render_with_game(menu_data, game)
        else:
            self.menu_render(menu_data)

    def menu_render(self, menu_data):
        title = menu_data.title
        pyxel.text(title.position[0], title.position[1], title.content, title.color)
        selection_color = 11
        items = menu_data.items_to_draw()
        current_selection = menu_data.get_current_selection()
        for text in items:
            x = text.position[0]
            if current_selection.text == text:
                pyxel.text(x + 8, text.position[1], "> " + text.content, selection_color)
            else:
                pyxel.text(x, text.position[1], text.content, text.color)

    def render_with_game(self, menu_data, game):
        # draw a dark rectangle over the game for menu background

        # draw a little window to the character?
        player = game.context.data_context.player_data
        position_x = pyxel.width // 4 - 20
        position_y = pyxel.height - 20

        pyxel.text(position_x - 8, position_y - 12, "Player", 7)
        draw_entity(player, position_x, position_y)

        if player.weapon:
            position_x = position_x + 28
            position_y = position_y
            weapon_type = str(player.weapon.category.name)
            weapon_type = weapon_type.replace("_", " ")
            pyxel.text(position_x - 8, position_y - 12, weapon_type, 7)
            draw_weapon(player, position_x, position_y)
            position_x = position_x + 12
        if player.shield:
            position_x = position_x + 32
            position_y = position_y
            shield_type = str(player.shield.shield_category.name)
            shield_type = shield_type.replace("_", " ")
            pyxel.text(position_x - 8, position_y - 12, shield_type, 7)
            draw_shield(player, position_x, position_y)
            position_x = position_x + 8




         # draw the menu on top



        self.render(menu_data)
