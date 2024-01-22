import abc


class Shape(abc.ABC):
    id_counter = 0

    def __init__(self, color, vertices, is_draw_border=True, is_visible=True):
        self.id = Shape.generate_id()
        self.color = color
        self.vertices = vertices
        self.is_draw_border = is_draw_border
        self.is_visible = is_visible

    def get_shape_id(self):
        return self.id

    def set_is_draw_border(self, is_draw_border):
        self.is_draw_border = is_draw_border

    def set_is_visible(self, is_visible):
        self.is_visible = is_visible

    @staticmethod
    def generate_id():
        Shape.id_counter += 1
        return Shape.id_counter

    @abc.abstractmethod
    def draw(self):
        pass
