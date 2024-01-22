from opengl_shape.entity.rectangle import Rectangle
from opengl_shape.entity.shape_scene import ShapeDrawerScene
from opengl_shape.repository.opengl_shape_drawer_repository import OpenGLShapeDrawerRepository

from OpenGL.GL import *


class OpenglShapeDrawerRepositoryImpl(OpenGLShapeDrawerRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def draw_shapes(self, shapes):
        print("OpenGLShapeDrawerRepositoryImpl: draw_shapes()")





