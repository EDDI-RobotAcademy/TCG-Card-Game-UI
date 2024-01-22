import abc


class OpenGLShapeDrawerRepository(abc.ABC):
    @abc.abstractmethod
    def draw_shapes(self):
        pass


