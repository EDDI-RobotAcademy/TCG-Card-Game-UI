from tests.opengl_shape_legacy.repository.shape_repository_impl import ShapeRepositoryImpl
from tests.opengl_shape_legacy.service.opengl_shape_service import OpenglShapeDrawerService


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

    def create_circle(self, color, center_vertex, radius):
        print("OpenglShapeDrawerServiceImpl: create_circle()")
        return self.__shapeRepository.create_rectangle(color, center_vertex, radius)

    def create_image(self, color, vertices, image_path):
        print("OpenglShapeDrawerServiceImpl: create_image()")
        return self.__shapeRepository.create_rectangle(color, vertices, image_path)

    def get_shape_drawer_scene(self):
        print("OpenglShapeDrawerServiceImpl: get_shape_drawer_scene()")
        return self.__shapeRepository.get_opengl_shape_drawer_scene()

    def process_border(self, shape_id, is_drawer_border):
        print("OpenglShapeDrawerServiceImpl: process_border()")
        self.__shapeRepository.process_border(shape_id, is_drawer_border)

    def set_shape_visible(self, shape_id, is_visible):
        print("OpenglShapeDrawerServiceImpl: set_shape_visible()")
        self.__shapeRepository.set_shape_visible(shape_id, is_visible)

    def set_local_translation(self, shape_id, local_translation):
        print("OpenglShapeDrawerServiceImpl: set_local_translation()")
        self.__shapeRepository.set_local_translation(shape_id, local_translation)

    def set_color_gradient(self, shape_id, is_color_gradient):
        print("OpenglShapeDrawerServiceImpl: set_color_gradient()")
        self.__shapeRepository.set_color_gradient(shape_id, is_color_gradient)











