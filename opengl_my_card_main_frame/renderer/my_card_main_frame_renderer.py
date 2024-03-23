from OpenGL import GL

from opengl_my_card_main_frame.infra.my_card_repository import MyCardRepository

from OpenGL.GL import *
from OpenGL.GLU import *


class MyCardMainFrameRenderer:

    my_card_repository = MyCardRepository.getInstance()

    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def render(self):
        # print("my card main frame 렌더러 호출")
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # 배경 및 사이드에 있는 나의 덱 화면
        for image_element in self.scene.my_card_background:
            self._render_shape(image_element)

        # # 나의 카드 텍스트
        # for text in self.scene.text_list[:8]:
        #     if text is None:
        #         pass
        #     else:
        #         self._render_shape(text)
        #
        # # 버튼 도형
        # # for button in self.scene.button_list:
        # #     self._render_shape(button)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if self.scene.go_back_button:
            self.scene.go_back_button.draw()

        if self.scene.create_deck_button:
            self.scene.create_deck_button.draw()

        glDisable(GL_BLEND)

        for my_card in self.my_card_repository.get_my_card_object_list_from_current_page():
            my_card_pickable_base = my_card.get_pickable_card_base()
            my_card_pickable_base.draw()

            my_card_attached_shape_list = my_card_pickable_base.get_attached_shapes()
            for my_card_attached_shape in my_card_attached_shape_list:
                my_card_attached_shape.draw()

        for my_card_count in self.my_card_repository.get_my_card_count_object_list_from_current_page():
            # print(f"my_card_count: {my_card_count}")
            my_card_count.draw()

        if self.scene.next_button:
            self.scene.next_button.draw()

        if self.scene.prev_button:
            self.scene.prev_button.draw()

        current_page_object = self.my_card_repository.get_current_page_object()
        current_page_number_object = current_page_object.get_current_page_number()
        if current_page_number_object:
            current_page_number_object.draw()

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()