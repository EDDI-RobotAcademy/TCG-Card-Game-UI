from opengl_shape.rectangle import Rectangle


class AlphaRectangle:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.background_rectangle = Rectangle(color=(0.0, 0.0, 0.0, 0),
                                              vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])

    def set_background_alpha(self, alpha):
        self.background_rectangle.set_alpha(alpha)

    def local_translate(self, local_translate):
        self.background_rectangle.local_translate(local_translate)

    def draw(self):
        self.background_rectangle.draw()
