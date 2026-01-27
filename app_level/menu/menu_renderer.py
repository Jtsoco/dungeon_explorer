import pyxel
from HUD.player_draw import draw_entity, draw_weapon, draw_shield, draw_only_shield, draw_only_weapon
from app_level.app_enums import MenuState
from app_level.menu.menu_option import ItemMenuOption
from enums.entity_enums import InventoryCategory as IC
class MenuRenderer():

    def __init__(self):
        pass

    def render(self, menu_data, game=None):
        if menu_data.menu_type == MenuState.PAUSE_MENU and game:
            pyxel.rect(0, 0, pyxel.width, pyxel.height, 0)
            self.menu_render(menu_data)
            self.render_with_game(menu_data, game)
            self.render_inventory(menu_data, game)
        else:
            self.draw_background()
            self.menu_render(menu_data)
            self.draw_character_select(menu_data)

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


    def draw_character_select(self, menu_data):
        characters = menu_data.get_characters_to_draw()
        # should only be one character in this
        position_x = pyxel.width // 4 - 20
        position_y = pyxel.height - 16
        for character in characters:
            self.render_character_with_weapons(character, position_x, position_y, text_y = 16)

    def render_character_with_weapons(self, character, position_x, position_y, text_y = None):
        if text_y is None:
            text_y = position_y - 12
        else:
            text_y = position_y - text_y
        pyxel.text(position_x - 8, text_y, "Player", 7)
        draw_entity(character, position_x, position_y)

        if character.weapon:
            position_x = position_x + 28
            position_y = position_y
            weapon_type = str(character.weapon.category.name)
            weapon_type = weapon_type.replace("_", " ")
            pyxel.text(position_x - 8, text_y, weapon_type, 7)
            draw_weapon(character, position_x, position_y)
            position_x = position_x + 12
        if character.shield:
            position_x = position_x + 32
            position_y = position_y
            shield_type = str(character.shield.shield_category.name)
            shield_type = shield_type.replace("_", " ")
            pyxel.text(position_x - 8, text_y, shield_type, 7)
            draw_shield(character, position_x, position_y)
            position_x = position_x + 8

    def render_with_game(self, menu_data, game):
        # draw a dark rectangle over the game for menu background

        # draw a little window to the character?
        player = game.context.data_context.player_data
        position_x = pyxel.width // 4 - 20
        position_y = pyxel.height - 20
        self.render_character_with_weapons(player, position_x, position_y)






         # draw the menu on top





    def draw_background(self, option=0):
        width = pyxel.width
        height = pyxel.height
        x = 240 * 8
        y = option * 8
        pyxel.bltm(0, 0, 0, x, y, width, height)

    def render_inventory(self, menu_data, game):
        horizontal = menu_data.get_horizontal_components()
        for component in horizontal:
            current_horizontal_selection = component.get_current_horizontal_selection()
            options = component.horizontal_options
            position_x = component.position[0] + 48
            position_y = component.position[1]
            for option in options:
                if isinstance(option, ItemMenuOption):

                    action = option.action
                    line = current_horizontal_selection == option
                    if action == MenuState.WEAPON_SELECT:
                        draw_only_weapon(option.item, position_x, position_y, line=line)
                    elif action == MenuState.SHIELD_SELECT:
                        draw_only_shield(option.item, position_x, position_y, line=line)
                    position_x += 8
