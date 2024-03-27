from opengl_button.button_service.again_no_button import AgainNoButton
from opengl_button.button_service.again_yes_button import AgainYesButton
from opengl_button.button_service.back_to_shop import BackToShopFrame
from opengl_button.button_service.draw_again_button import DrawAgainButton
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl

class BuyRandomCardFrameButtonBind:
    def __init__(self, master, frame):
        self.master = master
        self.buy_random_card_frame = frame
        self.ui_frame_service = UiFrameServiceImpl.getInstance()

        self.back_to_shop_frame_event_handler = BackToShopFrame(self.master, self.buy_random_card_frame)
        self.again_button_handler = DrawAgainButton(self.master, self.buy_random_card_frame)
        self.again_no_button_handler = AgainNoButton(self.master, self.buy_random_card_frame)
        self.again_yes_button_handler = AgainYesButton(self.master, self.buy_random_card_frame)

    def button_bind(self):
        print("마우스 클릭 이벤트들 바인드")
        self.buy_random_card_frame.bind("<Button-1>", self.combined_mouse_click_event)

    def combined_mouse_click_event(self, event):
        x, y = event.x, event.y
        print(f"x: {x}, y: {y}")

        self.back_to_shop_frame_event_handler.mouse_click_event(event)
        self.again_button_handler.mouse_click_event(event)
        self.again_no_button_handler.mouse_click_event(event)
        self.again_yes_button_handler.mouse_click_event(event)
