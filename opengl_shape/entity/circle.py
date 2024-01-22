from opengl_shape.entity.shape import Shape


class Circle(Shape):
    def __init__(self, color, center, radius):
        super().__init__(color, [center])
        self.radius = radius
        self.draw_border = True
