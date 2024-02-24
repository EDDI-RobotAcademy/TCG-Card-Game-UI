from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field_function.controller.battle_field_function_controller_impl import BattleFieldFunctionControllerImpl
from battle_field_ui_button.battle_field_button import BattleFieldButton
from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class GameEndPanel:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __battle_field_repository = BattleFieldRepository.getInstance()
    __battle_field_function_controller = BattleFieldFunctionControllerImpl.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_game_end_panel_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_game_end_panel(self, is_win):
        win_panel = RectangleImage(self.__pre_drawed_image_instance.get_pre_draw_your_card_deck(),
                                   vertices=[(750, 200), (1150, 200), (1150, 700), (750, 700)])
        self.add_shape(win_panel)

        text_vertices = [(850, 250), (1050, 250), (1050, 400), (850, 400)]
        if is_win:
            text_image = RectangleImage(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_win_text(),
                vertices=text_vertices
            )
        else:
            text_image = RectangleImage(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_lose_text(),
                vertices=text_vertices
            )
        self.add_shape(text_image)

    def init_shapes(self):
        self.create_game_end_panel(is_win=self.__battle_field_repository.is_win)


class GameEndConfirmButton:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __battle_field_function_controller = BattleFieldFunctionControllerImpl.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_confirm_button(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_confirm_button(self, image_data, vertices):
        confirm_button = BattleFieldButton(image_data=image_data,
                                            vertices=vertices)
        self.add_shape(confirm_button)
        return confirm_button

    def init_shapes(self):
        self.button_base = (
            self.create_confirm_button(image_data=self.__pre_drawed_image_instance.get_pre_draw_confirm_button(),
                vertices=[(850, 490), (1050, 490), (1050, 590), (850, 590)]))

    def get_button_base(self):
        return self.button_base

    def invoke_click_event(self):
        print("confirm_button.invoke_click_event!!!!")
        self.__battle_field_function_controller.callGameEndReward()