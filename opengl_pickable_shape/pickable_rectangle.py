
from opengl_shape.rectangle import Rectangle


class PickableRectangle(Rectangle):
    def __init__(self, color, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(color, vertices, global_translation, local_translation)

        self.attached_shapes = []

    # def set_attached_shapes(self, shape):
    #     self.attached_shapes.append(shape)

    # def get_attached_shapes(self):
    #     return self.attached_shapes

    # def is_point_inside(self, point):
    #     x, y = point
    #     y *= -1
    #
    #     if not (self.vertices[0][0] + self.global_translation[0] + self.local_translation[0] <= x <=
    #             self.vertices[2][0] + self.global_translation[0] + self.local_translation[0] and
    #             self.vertices[0][1] + self.global_translation[1] + self.local_translation[1] <= y <=
    #             self.vertices[2][1] + self.global_translation[1] + self.local_translation[1]):
    #         return False
    #
    #     winding_number = 0
    #     j = len(self.vertices) - 1
    #     for i in range(len(self.vertices)):
    #         if i < len(self.vertices):
    #             x1, y1 = self.vertices[j]
    #             x2, y2 = self.vertices[i]
    #
    #             if y1 + self.global_translation[1] + self.local_translation[1] <= y < y2 + self.global_translation[1] + \
    #                     self.local_translation[1] or \
    #                     y2 + self.global_translation[1] + self.local_translation[1] <= y < y1 + self.global_translation[
    #                 1] + self.local_translation[1]:
    #
    #                 if x1 + self.global_translation[0] + self.local_translation[0] + (
    #                         y - y1 - self.global_translation[1] - self.local_translation[1]) / (
    #                         y2 - y1) * (x2 - x1) > x:
    #                     winding_number = 1 - winding_number
    #
    #             j = i
    #
    #     return winding_number == 1

    def is_point_inside(self, point):
        x, y = point
        y *= -1

        print(f"is_point_inside -> x: {x}, y: {y}, local_translation: {self.local_translation}")
        print(f"vertices: {self.vertices}")

        translated_vertices = [
            (x * self.width_ratio + self.global_translation[0] + self.local_translation[0] * self.width_ratio,
             y * self.height_ratio + self.global_translation[1] + self.local_translation[1] * self.height_ratio)
            for x, y in self.vertices
        ]

        print(f"translated_vertices: {translated_vertices}")

        if not (translated_vertices[0][0] <= x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= y <= translated_vertices[2][1]):
            return False

        # count = 0
        # num_vertices = len(translated_vertices)
        #
        # for i in range(num_vertices):
        #     x1, y1 = translated_vertices[i]
        #     x2, y2 = translated_vertices[(i + 1) % num_vertices]
        #
        #     if ((y1 <= y < y2) or (y2 <= y < y1)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
        #         count += 1
        #
        # return count % 2 == 1

        return True


