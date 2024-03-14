from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class AnimationTestImage:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __current_animation_count = 0

    is_finished = False

    def __init__(self):
        self.animation_panel = None

        self.total_width = None
        self.total_height = None

        self.local_translation = (0, 0)

        self.width_ratio = 1
        self.height_ratio = 1

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def get_width_ratio(self):
        return self.width_ratio

    def set_width_ratio(self, width_ratio):
        self.width_ratio = width_ratio

    def get_height_ratio(self):
        return self.height_ratio

    def set_height_ratio(self, height_ratio):
        self.height_ratio = height_ratio

    def change_local_translation(self, _translation):
        # print("changed_local_translation: ", _translation)
        self.local_translation = _translation

    def get_animation_panel(self):
        return self.animation_panel

    def reset_animation_count(self):
        self.__current_animation_count = 0
        self.is_finished = False

    def draw_animation_panel(self):

        left_x_point = self.total_width * 0.4
        right_x_point = self.total_width * 0.6
        top_y_point = self.total_height * 0.65
        bottom_y_point = self.total_height * 0.35


        basic_fixed_card_base_vertices = [(-20, -25), (125, -25), (125, 195), (-20, 195)]

        self.animation_panel = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_animation(),
            # vertices=[
            #     (left_x_point, top_y_point),
            #     (right_x_point, top_y_point),
            #     (right_x_point, bottom_y_point),
            #     (left_x_point, bottom_y_point)
            # ],
             vertices=basic_fixed_card_base_vertices,
           local_translation=self.local_translation

        )


        # self.animation_panel = RectangleImage(
        #     image_data=self.__pre_drawed_image.get_pre_draw_animation(),
        #     vertices=basic_fixed_card_base_vertices,
        # #    local_translation=self.local_translation
        #     )
    def update_animation_panel(self):
        try:
            if self.__current_animation_count > 64:
                self.is_finished = True
                return

            self.__current_animation_count += 1
            image_count = self.__current_animation_count % 16
            self.animation_panel.set_image_data(
                self.__pre_drawed_image.get_pre_draw_animation(image_count))
        except:
            self.is_finished = True


