import os

from colorama import Fore, Style

from image_shape.non_background_image import NonBackgroundImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from common.utility import get_project_root

from OpenGL.GL import *
from OpenGL.GLU import *


class EffectAnimation:
    __pre_drawed_image = PreDrawedImage.getInstance()
    __current_animation_count = 0

    is_finished = False


    def __init__(self):
        self.root_window = None
        self.animation_panel = None

        self.total_width = None
        self.total_height = None

        self.local_translation = (0, 0)

        self.width_ratio = 1
        self.height_ratio = 1
        self.animation_name = None
        self.animation_image_path = None
        self.total_animation_count = 0
        self.unit_index = None

    def set_unit_index(self, index):
        print('set index: ', index)
        self.unit_index = index

    def get_unit_index(self):
        print('index return~~~ ,', self.unit_index)
        return self.unit_index

    def set_animation_name(self, animation_name):
        print(animation_name)
        self.animation_name = animation_name
        image_dir = os.path.join(get_project_root(), "local_storage", "animation", self.animation_name)
        # image_dir = os.path.join(self.__project_root, "local_storage", "animation_for_test")
        file_list = os.listdir(image_dir)
        self.total_animation_count = len(file_list)

    def get_animation_name(self):
        return self.animation_name

    def set_root_window(self, root_window):
        self.root_window = root_window

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

    def draw_animation_panel_with_vertices(self, vertices):
        self.animation_panel = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_effect_animation(self.animation_name),
            # vertices=[
            #     (left_x_point, top_y_point),
            #     (right_x_point, top_y_point),
            #     (right_x_point, bottom_y_point),
            #     (left_x_point, bottom_y_point)
            # ],
            vertices=vertices,
            local_translation=self.local_translation

        )

    def draw_full_screen_animation_panel(self):
        left_x_point = 0
        top_y_point = 0
        right_x_point = self.total_width
        bottom_y_point = self.total_height

        # Create vertices for the animation panel
        full_screen_vertices = [(left_x_point, top_y_point),
                                (right_x_point, top_y_point),
                                (right_x_point, bottom_y_point),
                                (left_x_point, bottom_y_point)]

        self.animation_panel = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_effect_animation(self.animation_name),
            # vertices=[
            #     (left_x_point, top_y_point),
            #     (right_x_point, top_y_point),
            #     (right_x_point, bottom_y_point),
            #     (left_x_point, bottom_y_point)
            # ],
            vertices=full_screen_vertices,
            local_translation=self.local_translation

        )

    def draw_animation_panel(self):

        basic_fixed_card_base_vertices = [(-32.5, 0), (137.5, 0), (137.5, 170), (-32.5, 170)]
        self.animation_panel = NonBackgroundImage(
            image_data=self.__pre_drawed_image.get_pre_draw_effect_animation(self.animation_name),
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

    # S = 0.5 * a * 64 * 64 -> 2번 루프 (32번 쉐도우 볼)
    # S = 0.5 * a * 4096
    # S = a * 2048
    # a = need_to_move_acceleration_distance / 2048

    # source -> point_x: 1078, point_y: 628
    # target -> point_x: 921, point_y: 143

    # 속도 조절은 step_count로 64는 좀 느림 -> 영상으로 치면 Fourth Shadow Ball 속도에 대응함
    # 48 * 48 / 2 = 1152
    # 40 * 40 / 2 = 800

    def update_effect_animation_panel_with_acceleration(self, need_to_move_acceleration_distance, step_count):
        try:
            print(f"{Fore.RED}update_effect_animation_panel_with_acceleration -> {Fore.GREEN}step_count: {step_count}, total_animation_count: {self.total_animation_count}{Style.RESET_ALL}")
            if step_count == 40:
                self.is_finished = True
                return

            if self.__current_animation_count == 32:
                self.__current_animation_count = 1

            accel_dist_x, accel_dist_y = need_to_move_acceleration_distance
            accel_x = accel_dist_x / 800.0
            accel_y = accel_dist_y / 800.0

            # print(f"{Fore.RED}update_effect_animation_panel() -> self.__current_animation_count: {Fore.GREEN}{self.__current_animation_count}{Style.RESET_ALL}")
            self.__current_animation_count += 1
            # image_count = self.__current_animation_count % 16
            image_count = self.__current_animation_count
            self.animation_panel.set_image_data(
                self.__pre_drawed_image.get_pre_draw_effect_animation(self.animation_name, image_count))

            new_vertices = [
                (vx - accel_x * step_count, vy - accel_y * step_count) for vx, vy in self.animation_panel.vertices
            ]
            self.animation_panel.update_vertices(new_vertices)
            print(f"{Fore.RED}self.animation_panel.vertices: {Fore.GREEN}{self.animation_panel.get_vertices()}{Style.RESET_ALL}")
        except:
            self.is_finished = True

    def update_effect_animation_panel(self):
        try:
            if self.__current_animation_count == self.total_animation_count:
                self.is_finished = True
                return

            # print(f"{Fore.RED}update_effect_animation_panel() -> self.__current_animation_count: {Fore.GREEN}{self.__current_animation_count}{Style.RESET_ALL}")
            self.__current_animation_count += 1
            # image_count = self.__current_animation_count % 16
            image_count = self.__current_animation_count
            self.animation_panel.set_image_data(
                self.__pre_drawed_image.get_pre_draw_effect_animation(self.animation_name, image_count))

            # glEnable(GL_BLEND)
            # # glBlendFunc(GL_SRC_ALPHA, GL_ONE)
            # # glBlendFunc(GL_ONE, GL_ZERO)
            # # glBlendFunc(GL_ZERO, GL_ONE)
            # # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # glBlendFunc(GL_ONE, GL_ONE)
            #
            # self.animation_panel.draw()
            #
            # glDisable(GL_BLEND)
        except:
            self.is_finished = True

    def update_harmful_effect_animation_panel(self):
        if self.__current_animation_count >= self.total_animation_count-1:
            self.__current_animation_count = 0

            # print(f"{Fore.RED}update_effect_animation_panel() -> self.__current_animation_count: {Fore.GREEN}{self.__current_animation_count}{Style.RESET_ALL}")

        # image_count = self.__current_animation_count % 16
        image_count = self.__current_animation_count
        self.animation_panel.set_image_data(
            self.__pre_drawed_image.get_pre_draw_effect_animation(self.animation_name, image_count))

        self.__current_animation_count += 1

    def update_loading_animation_panel(self):
        if self.__current_animation_count >= 238:
            self.__current_animation_count = 223

            # print(f"{Fore.RED}update_effect_animation_panel() -> self.__current_animation_count: {Fore.GREEN}{self.__current_animation_count}{Style.RESET_ALL}")
        print(f'current_animation_count: {self.__current_animation_count}')
        # image_count = self.__current_animation_count % 16
        image_count = self.__current_animation_count
        self.animation_panel.set_image_data(
            self.__pre_drawed_image.get_pre_draw_effect_animation(self.animation_name, image_count))

        self.__current_animation_count += 1


    def animate(self):
        def animate():
            finish_list = []
            is_all_finished = False
            for _animation_test_image in self.animation_test_image_list:
                _animation_test_image.update_animation_panel()
                finish_list.append(_animation_test_image.is_finished)

            for finish in finish_list:
                if finish == False:
                    is_all_finished = False
                    break
                else:
                    is_all_finished = True

            if not is_all_finished:
                self.master.after(17, animate)
            else:
                self.animation_test_image_list = []
                self.animation_test_image_panel_list = []
                print("finish animation")

