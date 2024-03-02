import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from image_shape.circle_image import CircleImage
from image_shape.rectangle_image import RectangleImage
from image_shape.rectangle_kinds import RectangleKinds
from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from common.utility import get_project_root
from opengl_shape.circle import Circle
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from opengl_battle_field_card_controller.card_controller_impl import CardControllerImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class FixedFieldOpponentHandCard:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0)):
        self.fixed_card_base = None
        self.local_translation = local_translation
        self.index = 0

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_local_translation(self):
        return self.local_translation

    def get_fixed_card_base(self):
        return self.fixed_card_base


    def create_card_background_rectangle(self, image_data, vertices, local_translation):
        card_background_illustration = RectangleImage(image_data=image_data,
                                                      local_translation=local_translation,
                                                      vertices=vertices)
        return card_background_illustration

    def create_fixed_card_base_rectangle(self, color, vertices, local_translation):
        fixed_card_base = PickableRectangle(color=color,
                                            local_translation=local_translation,
                                            vertices=vertices)
        fixed_card_base.set_draw_gradient(True)
        return fixed_card_base

    def init_card(self):

        basic_fixed_card_base_vertices = [(0, 0), (105, 0), (105, 170), (0, 170)]

        self.fixed_card_base = (
            self.create_fixed_card_base_rectangle(
                color=(255.0, 255.0, 255.0, 1.0),
                local_translation=self.local_translation,
                vertices=basic_fixed_card_base_vertices
            )
        )

        self.fixed_card_base.set_attached_shapes(
            self.create_card_background_rectangle(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_card_back_frame(),
                local_translation=self.local_translation,
                vertices=basic_fixed_card_base_vertices
            )
        )