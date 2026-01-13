import pyxel
class MenuRenderer():

    def __init__(self):
        pass

    def render(self, menu_data):
        title = menu_data.title
        pyxel.text(title.position[0], title.position[1], title.content, title.color)
        selection_color = 11
        for index, option in enumerate(menu_data.menu_options):
            x = option.text.position[0]
            if index == menu_data.current_selection_index:
                pyxel.text(x + 8, option.text.position[1], "> " + option.text.content, selection_color)
            else:
                pyxel.text(x, option.text.position[1], option.text.content, option.text.color)
