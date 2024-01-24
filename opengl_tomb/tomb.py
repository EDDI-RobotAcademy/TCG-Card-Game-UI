from opengl_shape.image_element import ImageElement
from opengl_shape.rectangle import Rectangle


class Tomb:
    __imagePath = None

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
    def get_tomb_shapes(self):
        return self.shapes
    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def create_tomb_rectangle(self, color, vertices):
        tomb_base = Rectangle(color=color,
                                       vertices=vertices)
        tomb_base.set_visible(True)
        self.add_shape(tomb_base)

    def create_illustration(self, image_path, vertices):
        unit_illustration = ImageElement(image_path=image_path,
                                         vertices=vertices)
        self.add_shape(unit_illustration)


    def init_shapes(self, image_path):
        self.__imagePath = image_path
        self.create_tomb_rectangle(color=(0.6, 0.4, 0.6, 1.0),
                                   vertices=[(50, 50), (200, 50), (200, 250), (50, 250)])

        self.create_illustration(image_path=self.__imagePath,
                                 vertices=[(50, 50), (200, 50), (200, 250), (50, 250)])