from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from screeninfo import get_monitors

from battle_field.entity.effect_animation import EffectAnimation
from common.utility import get_project_root
from image_shape.non_background_image import NonBackgroundImage
from image_shape.rectangle_image import RectangleImage
from opengl_buy_random_card_frame.entity.buy_random_card_scene import BuyRandomCardScene

from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard
from opengl_buy_random_card_frame.renderer.buy_random_card_frame_renderer import BuyRandomCardFrameRenderer
from opengl_shape.image_rectangle_element import ImageRectangleElement
from opengl_shape.rectangle import Rectangle
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class BuyRandomCardFrame(OpenGLFrame):
    __instance = None

    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    buy_check_repository = BuyCheckRepositoryImpl.getInstance()

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.animation_finished = False

        self.card_drawing_animation = None
        self.card_drawing_animation_panel = None



        self.init_monitor_specification()

        self.buy_random_card_scene = BuyRandomCardScene()

        self.current_rely = 0.20

        self.response_card_number = []

        self.redraw_check = False

        self.render = None

        self.current_width = None
        self.current_height = None

        self.width_ratio = 1
        self.height_ratio = 1

        self.prev_width = self.current_width
        self.prev_height = self.current_height

        self.is_reshape_not_complete = True

        self.bind("<Configure>", self.on_resize)

    def init_monitor_specification(self):
        print(f"init_monitor_specification()")

        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        self.width = target_monitor.width
        self.height = target_monitor.height

        self.is_reshape_not_complete = True

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height

        self.width_ratio = 1.0
        self.height_ratio = 1.0


    def initgl(self):
        print("initgl 입니다.")
        # glClearColor(0, 0, 0, 0)
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        # self.make_card_main_frame()
        # self.render = BuyRandomCardFrameRenderer(self.buy_random_card_scene, self)
        # self.render.render()

        # self.tkMakeCurrent()

    def init_first_window(self, width, height):
        print(f"buy_random_card_frame() - Operate Only Once -> width: {width}, height: {height}")
        self.width = width
        self.height = height

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height
        self.is_reshape_not_complete = False

        self.buy_check_repository.set_total_window_size(self.width, self.height)

        self.card_drawing_animation = EffectAnimation()
        self.card_drawing_animation.set_total_window_size(self.width, self.height)
        self.card_drawing_animation.set_animation_name('card_drawing_scene')
        self.card_drawing_animation.draw_full_screen_animation_panel()
        self.card_drawing_animation_panel = self.card_drawing_animation.get_animation_panel()



        self.make_card_main_frame()
        self.render = BuyRandomCardFrameRenderer(self.buy_random_card_scene, self)

        self.buy_check_repository.create_random_buy_list()

        self.render.set_effect_animation(self.card_drawing_animation)

        # self.play_card_drawing_effect_animation()



    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")

        if self.is_reshape_not_complete:
            self.init_first_window(width, height)

        self.current_width = width
        self.current_height = height

        self.width_ratio = self.current_width / self.prev_width
        self.height_ratio = self.current_height / self.prev_height

        self.width_ratio = min(self.width_ratio, 1.0)
        self.height_ratio = min(self.height_ratio, 1.0)

        self.prev_width = self.current_width
        self.prev_height = self.current_height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)


    def make_card_main_frame(self):
        project_root = get_project_root()
        glClearColor(0.0, 1.0, 0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # 나의 카드 배경 화면
        # background_rectangle = ImageRectangleElement(image_path=os.path.join(project_root, "local_storage", "image", "battle_lobby", "background.png"),
        #                                              local_translation=(0, 0),
        #                                              vertices=[(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])

        self.__pre_drawed_image_instance.pre_draw_buy_random_background(self.width, self.height)
        background_data = self.__pre_drawed_image_instance.get_pre_drawed_buy_random_background()
        background_rectangle = RectangleImage(image_data=background_data,
                                              vertices=[
                                                  (0, 0),
                                                  (self.width, 0),
                                                  (self.width, self.height),
                                                  (0, self.height)])

        self.buy_random_card_scene.add_buy_random_background(background_rectangle)


        # 뒤로가기 버튼
        go_to_back_button = Rectangle(color=(1.0, 1.0, 1.0, 0.0),
                                      local_translation=(0, 0),
                                      vertices=[(0.9016216 * self.width, 0.1978346 * self.height),
                                                (0.97567567 * self.width, 0.1978346 * self.height),
                                                (0.97567567 * self.width, 0.258858 * self.height),
                                                (0.9016216 * self.width, 0.258858 * self.height)])
        go_to_back_button.set_draw_border(False)
        self.buy_random_card_scene.add_go_to_back_button(go_to_back_button)

        again_button = Rectangle(color=(1.0, 1.0, 1.0, 0.0),
                                 local_translation=(0, 0),
                                 vertices=[(0.9016216 * self.width, 0.1092519685 * self.height),
                                           (0.97567567 * self.width, 0.1092519685 * self.height),
                                           (0.97567567 * self.width, 0.17716535 * self.height),
                                           (0.9016216 * self.width, 0.17716535 * self.height)])
        again_button.set_draw_border(False)
        self.buy_random_card_scene.add_again_button(again_button)

        self.response_card_number = BuyCheckRepositoryImpl.getInstance().getRandomCardList()
        print(f"response_card_number: {self.response_card_number}")

        # 다시 실행 팝업창
        try_again_screen_left_x_point = self.width * 0.268
        try_again_screen_right_x_point = self.width * 0.683
        try_again_screen_top_y_point = self.height * 0.276
        try_again_screen_bottom_y_point = self.height * 0.672
        try_again_image_data = self.__pre_drawed_image_instance.get_pre_draw_try_again_screen()
        try_again_screen = NonBackgroundImage(image_data=try_again_image_data,
                                              vertices=[
                                                  (try_again_screen_left_x_point, try_again_screen_top_y_point),
                                                  (try_again_screen_right_x_point, try_again_screen_top_y_point),
                                                  (try_again_screen_right_x_point, try_again_screen_bottom_y_point),
                                                  (try_again_screen_left_x_point, try_again_screen_bottom_y_point)
                                              ])
        self.buy_random_card_scene.add_try_again_screen(try_again_screen)

        # 예 버튼
        yes_button_left_x_point = self.width * 0.356
        yes_button_right_x_point = self.width * 0.44
        yes_button_top_y_point = self.height * 0.575
        yes_button_bottom_y_point = self.height * 0.629
        yes_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_yes_button()
        yes_button = NonBackgroundImage(image_data=yes_button_image_data,
                                        vertices=[
                                            (yes_button_left_x_point, yes_button_top_y_point),
                                            (yes_button_right_x_point, yes_button_top_y_point),
                                            (yes_button_right_x_point, yes_button_bottom_y_point),
                                            (yes_button_left_x_point, yes_button_bottom_y_point)
                                        ])
        self.buy_random_card_scene.add_yes_button(yes_button)

        # 아니오 버튼
        no_button_left_x_point = self.width * 0.512
        no_button_right_x_point = self.width * 0.596
        no_button_top_y_point = self.height * 0.575
        no_button_bottom_y_point = self.height * 0.629
        no_button_image_data = self.__pre_drawed_image_instance.get_pre_draw_no_button()
        no_button = NonBackgroundImage(image_data=no_button_image_data,
                                        vertices=[
                                            (no_button_left_x_point, no_button_top_y_point),
                                            (no_button_right_x_point, no_button_top_y_point),
                                            (no_button_right_x_point, no_button_bottom_y_point),
                                            (no_button_left_x_point, no_button_bottom_y_point)
                                        ])
        self.buy_random_card_scene.add_no_button(no_button)

        # x = 200
        # y = 200
        #
        # for i, number in enumerate(self.response_card_number):
        #     try:
        #         print(f"index: {i}, card number: {number}")
        #         card = LegacyPickableCard(local_translation=(x, y), scale=800)
        #         card.init_card(number)
        #         self.buy_random_card_scene.add_card_list(card)
        #         #print(f"카드 리스트: {self.buy_random_card_scene.get_card_list()}")
        #
        #         x += 300
        #
        #         if (i + 1) % 5 == 0:
        #             x = 200
        #             y = 500
        #             if (i + 1) % 10 == 0:
        #                 x = 200
        #                 y = 50
        #
        #         if (i + 1) % 10 == 0:
        #             continue
        #
        #     except Exception as e:
        #         print(f"Error creating card: {e}")
        #         pass


    def redraw(self):
        if self.is_reshape_not_complete:
            return

        if self.card_drawing_animation_panel:
            if self.card_drawing_animation.is_finished:
                self.animation_finished = True
                self.card_drawing_animation_panel = None
                self.card_drawing_animation = None

            else:
                self.card_drawing_animation.set_width_ratio(self.width_ratio)
                self.card_drawing_animation.set_height_ratio(self.height_ratio)
                self.card_drawing_animation.update_effect_animation_panel()
                # print('그리는중')
                # print(self.card_drawing_animation)
                # print(self.card_drawing_animation_panel)
                # self.card_drawing_animation.set_width_ratio(self.width_ratio)
                # self.card_drawing_animation.set_height_ratio(self.height_ratio)
                # self.card_drawing_animation.update_effect_animation_panel()
                # self.card_drawing_animation_panel.draw()



        self.render.render()
        


        # if self.redraw_check is True:
        #     self.make_card_main_frame()
        #     self.render_after = BuyRandomCardFrameRenderer(self.buy_random_card_scene, self)
        #     self.render_after.render()

    
    def play_card_drawing_effect_animation(self):
        def animate():
            self.card_drawing_animation.set_width_ratio(self.width_ratio)
            self.card_drawing_animation.set_height_ratio(self.height_ratio)
            self.card_drawing_animation.update_effect_animation_panel()
            self.card_drawing_animation_panel.draw()


            if not self.card_drawing_animation.is_finished:
                self.master.after(100, animate)
            else:
                print("drawing_effect_animation finish")
                self.animation_finished = True
                # self.card_drawing_animation_panel = None
                # self.card_drawing_animation = None

        self.card_drawing_animation.reset_animation_count()
        self.master.after(17, animate)