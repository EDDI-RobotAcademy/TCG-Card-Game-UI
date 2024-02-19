import abc


class Shape(abc.ABC):
    def __init__(self, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        self.vertices = vertices
        self.initial_vertices = None
        self.initial_center = None

        # self.width = 0
        # self.height = 0

        self.global_translation = global_translation
        self.local_translation = local_translation
        self.translation = self.local_translation + self.global_translation
        self.attached_shapes = []

    # def calculate_width_height(self):
    #     if len(self.vertices) == 4:
    #         x_values = [vertex[0] for vertex in self.vertices]
    #         y_values = [vertex[1] for vertex in self.vertices]
    #         width = max(x_values) - min(x_values)
    #         height = max(y_values) - min(y_values)
    #         return width, height
    #     else:
    #         raise ValueError("A rectangle should have exactly 4 vertices.")

    def set_initial_vertices(self, vertices):
        self.initial_vertices = vertices

    def get_initial_vertices(self):
        return self.initial_vertices

    def set_initial_center(self, vertices):
        self.initial_center = [vertices[0][0], vertices[0][1]]

    def get_initial_center(self):
        return self.initial_center

    def set_attached_shapes(self, shape):
        self.attached_shapes.append(shape)

    def get_attached_shapes(self):
        return self.attached_shapes

    def local_translate(self, local_translate):
        print(f"shape -> local_translate: {local_translate}")
        self.local_translation = local_translate

    def global_translate(self, global_translate):
        self.global_translation = global_translate

    def set_alpha(self, new_alpha):
        if len(self.color) == 4:
            self.color = self.color[:3] + (new_alpha,)
        else:
            self.color = self.color + (new_alpha,)

    def update_vertices(self, new_vertices):
        self.vertices = new_vertices

    def get_local_translation(self):
        return self.local_translation

    @abc.abstractmethod
    def draw(self):
        pass
