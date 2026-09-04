class Terrain:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Cover(Terrain):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)