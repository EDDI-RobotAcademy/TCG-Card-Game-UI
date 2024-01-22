from opengl_shape_drawer.entity.rectangle import Rectangle
from opengl_shape_drawer.entity.shape_drawer_scene import ShapeDrawerScene
from opengl_shape_drawer.repository.shape_repository import ShapeRepository


class ShapeRepositoryImpl(ShapeRepository):
    __instance = None
    __opengl_shape_drawer_scene = ShapeDrawerScene()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_opengl_shape_drawer_scene(self):
        print("ShapeRepositoryImpl: get_opengl_shape_drawer_scene()")
        return self.__opengl_shape_drawer_scene.get_shapes()

    def create_rectangle(self, color, vertices):
        print("ShapeRepositoryImpl: create_rectangle()")

        rectangle = Rectangle(color, vertices)
        self.__opengl_shape_drawer_scene.add_shape(rectangle)

