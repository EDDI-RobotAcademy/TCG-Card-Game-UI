from tests.opengl_shape_legacy.entity.shape import Shape


class ImageItem(Shape):
    def __init__(self,color, vertices, image_path):
        super().__init__(color, vertices)

        self.image_path = image_path

