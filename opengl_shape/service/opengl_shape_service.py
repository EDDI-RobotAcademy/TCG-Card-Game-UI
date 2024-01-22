import abc


class OpenglShapeDrawerService(abc.ABC):
    @abc.abstractmethod
    def create_rectangle(self, color, vertices):
        pass

    @abc.abstractmethod
    def create_circle(self, color, center_vertex, radius):
        pass

    @abc.abstractmethod
    def get_shape_drawer_scene(self):
        pass

    @abc.abstractmethod
    def process_border(self, shape_id, is_drawer_border):
        pass

    @abc.abstractmethod
    def set_shape_visible(self, shape_id, is_visible):
        pass

    @abc.abstractmethod
    def set_local_translation(self, shape_id, local_translation):
        pass

    @abc.abstractmethod
    def set_color_gradient(self, shape_id, is_color_gradient):
        pass
