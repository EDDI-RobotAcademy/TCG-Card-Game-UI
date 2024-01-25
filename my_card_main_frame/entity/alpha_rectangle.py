from opengl_shape.rectangle import Rectangle


class AlphaRectangle:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.is_visible = True
        self.background_rectangle = Rectangle(color=(0.0, 0.0, 0.0, 0),
                                              vertices=[(0, 0), (self.width, 0), (self.width, self.height),
                                                        (0, self.height)])

    def set_background_alpha(self, alpha):
        self.background_rectangle.set_alpha(alpha)

    # def draw(self):
    #     self.background_rectangle.draw()

    def draw(self):
        if self.is_visible:
            self.background_rectangle.draw()

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible