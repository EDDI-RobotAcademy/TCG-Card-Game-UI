from OpenGL import GL

from OpenGL.GL import *
from OpenGL.GLU import *

from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl


class BuyRandomCardFrameRenderer:

    buy_check_repository = BuyCheckRepositoryImpl.getInstance()

    def __init__(self, scene, window):
        self.scene = scene
        self.window = window
        self.try_again_screen_visible = False

    def render(self):
        # print("buy random card frame 렌더러 호출")
        self.window.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # 배경 및 사이드에 있는 나의 덱 화면
        # for image_element in self.scene.my_card_background:
        #     print(f"이미지 그리기: {image_element}")
        #     self._render_shape(image_element)
        if self.scene.buy_random_background:
            self.scene.buy_random_background.draw()

        # # 버튼 도형
        # for button in self.scene.button_list:
        #     # print(f"버튼 그리기: {button}")
        #     self._render_shape(button)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if self.scene.go_to_back_button:
            self.scene.go_to_back_button.draw()

        if self.scene.again_button:
            self.scene.again_button.draw()

        # glDisable(GL_BLEND)

        # for card in self.scene.card_list[:10]:
        #     # print(f"카드 리스트 몇 개임? {len(self.scene.card_list[:10])}")
        #     attached_tool_card = card.get_tool_card()
        #     attached_tool_card.draw()
        #
        #     pickable_card_base = card.get_pickable_card_base()
        #     pickable_card_base.draw()
        #
        #     attached_shape_list = pickable_card_base.get_attached_shapes()
        #     for attached_shape in attached_shape_list:
        #         attached_shape.draw()

        if self.buy_check_repository.get_need_to_redraw():
            self.buy_check_repository.set_need_to_redraw(False)

            self.buy_check_repository.create_random_buy_list()

        for card in self.buy_check_repository.get_random_buy_card_object_list():
            pickable_card_base = card.get_pickable_card_base()
            pickable_card_base.draw()

            attached_shape_list = pickable_card_base.get_attached_shapes()
            for attached_shape in attached_shape_list:
                attached_shape.draw()

        if self.buy_check_repository.get_try_again_screen_visible() == True:
            self.scene.try_again_screen.draw()
            self.scene.yes_button.draw()
            self.scene.no_button.draw()

        self.window.tkSwapBuffers()

    def _render_shape(self, shape):
        shape.draw()