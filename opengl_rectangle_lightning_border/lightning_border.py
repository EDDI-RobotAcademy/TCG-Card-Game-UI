from opengl_lightning_generator.lightning_generator import LightningGenerator


class LightningBorder:
    def __init__(self):
        self.shape = None
        self.padding = 0
        self.lightning_generator = LightningGenerator()
        self.lightning_segments = []

        self.width_ratio = 1
        self.height_ratio = 1

    def set_width_ratio(self, width_ratio):
        self.width_ratio = width_ratio

    def set_height_ratio(self, height_ratio):
        self.height_ratio = height_ratio

    def set_padding(self, padding):
        self.padding = padding

    def update_shape(self, shape):
        self.shape = shape
        self.generate_lightning_border()

    def generate_lightning_border(self):
        shape = self.shape
        local_translation = shape.get_local_translation()
        self.padding *= self.width_ratio

        self.lightning_segments = self.lightning_generator.generate_lightning(
            (
                shape.vertices[0][0] * self.width_ratio + local_translation[0] * self.width_ratio - self.padding,
                shape.vertices[0][1] * self.height_ratio + local_translation[1] * self.height_ratio - self.padding
            ),
            (
                shape.vertices[2][0] * self.width_ratio + local_translation[0] * self.width_ratio + self.padding,
                shape.vertices[0][1] * self.height_ratio + local_translation[1] * self.height_ratio - self.padding
            ),
            10, 5, 0.2, 0.7)

        self.lightning_segments.extend(self.lightning_generator.generate_lightning(
            (
                shape.vertices[2][0] * self.width_ratio + local_translation[0] * self.width_ratio + self.padding,
                shape.vertices[0][1] * self.height_ratio + local_translation[1] * self.height_ratio - self.padding
            ),
            (
                shape.vertices[2][0] * self.width_ratio + local_translation[0] * self.width_ratio + self.padding,
                shape.vertices[2][1] * self.height_ratio + local_translation[1] * self.height_ratio + self.padding
            ),
            10, 5, 0.2, 0.7))

        self.lightning_segments.extend(self.lightning_generator.generate_lightning(
            (
                shape.vertices[0][0] * self.width_ratio + local_translation[0] * self.width_ratio - self.padding,
                shape.vertices[2][1] * self.height_ratio + local_translation[1] * self.height_ratio + self.padding
            ),
            (
                shape.vertices[2][0] * self.width_ratio + local_translation[0] * self.width_ratio + self.padding,
                shape.vertices[2][1] * self.height_ratio + local_translation[1] * self.height_ratio + self.padding
            ),
            10, 5, 0.2, 0.7))

        self.lightning_segments.extend(self.lightning_generator.generate_lightning(
            (
                shape.vertices[0][0] * self.width_ratio + local_translation[0] * self.width_ratio - self.padding,
                shape.vertices[0][1] * self.height_ratio + local_translation[1] * self.height_ratio - self.padding
            ),
            (
                shape.vertices[0][0] * self.width_ratio + local_translation[0] * self.width_ratio - self.padding,
                shape.vertices[2][1] * self.height_ratio + local_translation[1] * self.height_ratio + self.padding
            ),
            10, 5, 0.2, 0.7))

    def draw_lightning_border(self):
        for segment in self.lightning_segments:
            self.lightning_generator.draw_lightning_segment(segment)
