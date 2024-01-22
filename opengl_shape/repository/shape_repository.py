import abc


class ShapeRepository(abc.ABC):
    @abc.abstractmethod
    def create_rectangle(self, color, vertices):
        pass

    @abc.abstractmethod
    def process_border(self, shape_id, is_draw_border):
        pass

    @abc.abstractmethod
    def set_shape_visible(self, shape_id, is_visible):
        pass

    @abc.abstractmethod
    def set_local_translation(self, shape_id, local_translation):
        pass



