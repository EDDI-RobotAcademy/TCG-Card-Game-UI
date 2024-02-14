import abc


class Shape(abc.ABC):
    def __init__(self, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        self.vertices = vertices
        self.global_translation = global_translation
        self.local_translation = local_translation
        self.translation = self.local_translation + self.global_translation

    def local_translate(self, local_translate):
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
