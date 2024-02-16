from opengl_button.button_service.back_to_shop import BackToShopFrame
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl

class BuyRandomCardFrameButtonBind:
    def __init__(self, master, frame):
        self.master = master
        self.my_card_main_frame = frame
        self.ui_frame_service = UiFrameServiceImpl.getInstance()

        self.back_to_shop_frame_event_handler = BackToShopFrame(self.master, self.my_card_main_frame)

    def button_bind(self):
        print("마우스 클릭 이벤트들 바인드")
        self.my_card_main_frame.bind("<Button-1>", self.combined_mouse_click_event)

    def combined_mouse_click_event(self, event):
        self.back_to_shop_frame_event_handler.mouse_click_event(event)
