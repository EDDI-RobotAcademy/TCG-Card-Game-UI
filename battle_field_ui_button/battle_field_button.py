from image_shape.rectangle_image import RectangleImage


class BattleFieldButton(RectangleImage):
    def __init__(self, image_data, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(image_data, vertices, global_translation, local_translation)

    def is_point_inside(self, point):
        x, y = point
        y *= -1

        translated_vertices = [
            (x + self.global_translation[0] + self.local_translation[0],
             y + self.global_translation[1] + self.local_translation[1])
            for x, y in self.vertices
        ]

        if not (translated_vertices[0][0] <= x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= y <= translated_vertices[2][1]):
            return False


        return True