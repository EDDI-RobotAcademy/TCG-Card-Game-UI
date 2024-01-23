from opengl_shape_legacy.entity.circle import Circle
from opengl_shape_legacy.entity.image_item import ImageItem
from opengl_shape_legacy.entity.rectangle import Rectangle
from opengl_shape_legacy.entity.shape_scene import ShapeDrawerScene
from opengl_shape_legacy.repository.shape_repository import ShapeRepository


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

        return rectangle.get_shape_id()

    def create_circle(self, color, center_vertex, radius):
        print("ShapeRepositoryImpl: create_circle()")

        circle = Circle(color, center_vertex, radius)
        self.__opengl_shape_drawer_scene.add_shape(circle)

        return circle.get_shape_id()

    def create_image(self, color, vertices, image_path):
        print("ShapeRepositoryImpl: create_image()")

        imageItem = ImageItem(color, vertices, image_path)
        self.__opengl_shape_drawer_scene.add_shape(imageItem)

        return imageItem.get_shape_id()

    def process_border(self, shape_id, is_draw_border):
        print("ShapeRepositoryImpl: process_border()")

        scene_shapes = self.get_opengl_shape_drawer_scene()
        for shape in scene_shapes:
            if shape_id == shape.get_shape_id():
                shape.set_is_draw_border(is_draw_border)

    def set_shape_visible(self, shape_id, is_visible):
        print("ShapeRepositoryImpl: set_shape_visible()")

        scene_shapes = self.get_opengl_shape_drawer_scene()
        for shape in scene_shapes:
            if shape_id == shape.get_shape_id():
                shape.set_is_visible(is_visible)

    def set_local_translation(self, shape_id, local_translation):
        print("ShapeRepositoryImpl: set_local_translation()")

        scene_shapes = self.get_opengl_shape_drawer_scene()
        for shape in scene_shapes:
            if shape_id == shape.get_shape_id():
                shape.set_local_translation(local_translation)

    def set_color_gradient(self, shape_id, is_color_gradient):
        print("ShapeRepositoryImpl: set_color_gradient()")

        scene_shapes = self.get_opengl_shape_drawer_scene()
        for shape in scene_shapes:
            if shape_id == shape.get_shape_id():
                shape.set_color_gradient(is_color_gradient)








