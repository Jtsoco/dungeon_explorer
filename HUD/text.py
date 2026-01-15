import pyxel

class Text():
    def __init__(self, content, position=(0, 0), color=7):
        self.content = content
        self.position = position
        self.color = color

        self.height = 8 #pyxel sets hight to be the same for all fonts at 8
    def draw(self):
        pyxel.text(self.position[0], self.position[1], self.content, self.color)
