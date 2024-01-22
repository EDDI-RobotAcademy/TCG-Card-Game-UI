import abc


class Shape(abc.ABC):
    id_counter = 0

    def __init__(self, color, vertices, local_translation=(0, 0),
                 is_draw_border=True, is_visible=True, is_color_gradient=False):
        self.id = Shape.generate_id()
        self.color = color
        self.vertices = vertices
        self.is_draw_border = is_draw_border
        self.is_visible = is_visible
        self.is_color_gradient = is_color_gradient
        self.local_translation = local_translation

    def get_shape_id(self):
        return self.id

    def set_is_draw_border(self, is_draw_border):
        self.is_draw_border = is_draw_border

    def set_is_visible(self, is_visible):
        self.is_visible = is_visible

    def set_color_gradient(self, is_color_gradient):
        self.is_color_gradient = is_color_gradient

    def set_local_translation(self, local_translation):
        self.local_translation = local_translation

    @staticmethod
    def generate_id():
        Shape.id_counter += 1
        return Shape.id_counter

    @abc.abstractmethod
    def draw(self):
        pass
