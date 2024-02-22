import os

from battle_field_function.controller.battle_field_function_controller_impl import BattleFieldFunctionControllerImpl
from battle_field_ui_button.battle_field_button import BattleFieldButton
from common.utility import get_project_root
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourTomb:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __battle_field_function_controller = BattleFieldFunctionControllerImpl.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_tomb = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale
        self.your_tomb_button_base = None

    def get_tomb_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_your_tomb_button(self, image_data, vertices):
        your_tomb_button = BattleFieldButton(image_data=image_data,
                                                vertices=vertices)
        self.add_shape(your_tomb_button)
        return your_tomb_button

    def init_shapes(self):
        self.your_tomb_button_base = (
            self.create_your_tomb_button(image_data=self.__pre_drawed_image_instance.get_pre_draw_your_tomb(),
                              vertices=[(1870, 1030), (1720, 1030), (1720, 830), (1870, 830)]))

    def get_button_base(self):
        return self.your_tomb_button_base

    def invoke_click_event(self):
        print("your_tomb_button.invoke_click_event!!!!")
        # self.__battle_field_function_controller.callTurnEnd()
