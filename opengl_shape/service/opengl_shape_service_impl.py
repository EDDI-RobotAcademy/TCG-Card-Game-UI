from opengl_shape.repository.shape_repository_impl import ShapeRepositoryImpl
from opengl_shape.service.opengl_shape_service import OpenglShapeDrawerService


class OpenglShapeDrawerServiceImpl(OpenglShapeDrawerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__shapeRepository = ShapeRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create_rectangle(self, color, vertices):
        print("OpenglShapeDrawerServiceImpl: create_rectangle()")
        return self.__shapeRepository.create_rectangle(color, vertices)

    def get_shape_drawer_scene(self):
        print("OpenglShapeDrawerServiceImpl: get_shape_drawer_scene()")
        return self.__shapeRepository.get_opengl_shape_drawer_scene()

    def process_border(self, shape_id, is_drawer_border):
        print("OpenglShapeDrawerServiceImpl: process_border()")
        return self.__shapeRepository.process_border(shape_id, is_drawer_border)







