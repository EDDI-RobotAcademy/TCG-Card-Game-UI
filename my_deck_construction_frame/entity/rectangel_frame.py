from opengl_shape.rectangle import Rectangle


class RectangleFrame:
    def __init__(self):
        self.is_visible = True
        self.rectangle = Rectangle(color=(0.5, 0.0, 0.0, 1.0),
                                   vertices=[(300, 260), (900, 260), (900, 520), (300, 520)])

    # def draw(self):
    #     self.rectangle.draw()

    def rectangle_draw(self):
        if self.is_visible:
            self.rectangle.draw()

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible