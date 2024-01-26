from opengl_shape.rectangle import Rectangle


class PickableRectangle(Rectangle):
    def __init__(self, color, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(color, vertices, global_translation, local_translation)

        self.attached_shapes = []

    def set_attached_shapes(self, shape):
        self.attached_shapes.append(shape)

    def get_attached_shapes(self):
        return self.attached_shapes

    def is_point_inside(self, point):
        print(f"is_point_inside() - point: {point}")
        x, y = point
        y *= -1

        # if not (self.vertices[0][0] + self.global_translation[0] + self.local_translation[0] <= x <=
        #         self.vertices[-2][0] + self.global_translation[0] + self.local_translation[0] and
        #         self.vertices[0][1] + self.global_translation[1] + self.local_translation[1] <= y <=
        #         self.vertices[-2][1] + self.global_translation[1] + self.local_translation[1]):
        #     print("마우스가 Picking 가능한 객체에 존재하지 않음: Fail")
        #     return False
        print(f"self.vertices: {self.vertices}")
        print(f"self.vertices[0][0] + global_translation[0] + local_translation[0]: "
              f"{self.vertices[0][0] + self.global_translation[0] + self.local_translation[0]}")
        print(f"self.vertices[2][0] + global_translation[0] + local_translation[0]: "
              f"{self.vertices[2][0] + self.global_translation[0] + self.local_translation[0]}")
        print(f"self.vertices[0][1] + global_translation[1] + local_translation[1]: "
              f"{self.vertices[0][1] + self.global_translation[1] + self.local_translation[1]}")
        print(f"self.vertices[2][1] + global_translation[1] + local_translation[1]: "
              f"{self.vertices[2][1] + self.global_translation[1] + self.local_translation[1]}")

        print(f"global_translation[0]: {self.global_translation[0]}, global_translation[1]: {self.global_translation[1]}")
        print(f"local_translation[0]: {self.local_translation[0]}, local_translation[1]: {self.local_translation[1]}")

        if not (self.vertices[0][0] + self.global_translation[0] + self.local_translation[0] <= x <=
                self.vertices[2][0] + self.global_translation[0] + self.local_translation[0] and
                self.vertices[0][1] + self.global_translation[1] + self.local_translation[1] <= y <=
                self.vertices[2][1] + self.global_translation[1] + self.local_translation[1]):
            return False

        print("calculate mouse inside the object")
        winding_number = 0
        j = len(self.vertices) - 1
        for i in range(len(self.vertices)):
            if i < len(self.vertices):
                x1, y1 = self.vertices[j]
                x2, y2 = self.vertices[i]

                if y1 + self.global_translation[1] + self.local_translation[1] <= y < y2 + self.global_translation[1] + \
                        self.local_translation[1] or \
                        y2 + self.global_translation[1] + self.local_translation[1] <= y < y1 + self.global_translation[
                    1] + self.local_translation[1]:

                    if x1 + self.global_translation[0] + self.local_translation[0] + (
                            y - y1 - self.global_translation[1] - self.local_translation[1]) / (
                            y2 - y1) * (x2 - x1) > x:
                        winding_number = 1 - winding_number

                j = i

        return winding_number == 1

