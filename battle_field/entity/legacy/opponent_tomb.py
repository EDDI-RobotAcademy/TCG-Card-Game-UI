import os

from common.utility import get_project_root
from image_shape.rectangle_image import RectangleImage
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.image_rectangle_element import ImageRectangleElement
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class OpponentTomb:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_tomb = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
        self.pickable_opponent_tomb_base = None

    def get_tomb_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)
    def get_pickable_opponent_tomb_base(self):
        return self.pickable_opponent_tomb_base
    def create_opponent_tomb(self, color, vertices, local_translation):
        pickable_opponent_tomb_base = PickableRectangle(color=color,
                                      local_translation=local_translation,
                                      vertices=vertices)
        self.add_shape(pickable_opponent_tomb_base)
        return pickable_opponent_tomb_base

    def create_illustration(self, image_path, vertices, local_translation):
        tomb_illustration = ImageRectangleElement(image_path=image_path,
                                                  local_translation=local_translation,
                                                  vertices=vertices)
        self.add_shape(tomb_illustration)
        return tomb_illustration

    def init_shapes(self):
        project_root = get_project_root()
        self.__imagePath = os.path.join(project_root, "local_storage", "image", "battle_field",
                                            "tomb.jpeg")

        self.pickable_opponent_tomb_base = (
            self.create_opponent_tomb(color=(0, 0, 0, 1.0),
                                            local_translation=self.local_translation,
                                            vertices=[(50, 50), (200, 50), (200, 250), (50, 250)]))

        # self.pickable_tomb_base.set_attached_shapes(
        #     self.create_illustration(image_path=self.__imagePath,
        #                              local_translation=self.local_translation,
        #                              vertices=[(50, 50), (200, 50), (200, 250), (50, 250)]))