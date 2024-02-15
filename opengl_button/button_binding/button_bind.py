from opengl_button.button_service.create_previous_page_screen import CreatePreviousPageScreen
from opengl_button.button_service.create_deck_register_button import CreateDeckRegisterButton
from opengl_button.button_service.create_deck_register_screen import CreateDeckRegisterScreen
from opengl_button.button_service.go_to_back_lobby_frame import GoToBackLobbyFrame
from opengl_button.button_service.next_page_screen import NextPageScreen
from opengl_button.button_service.page_manager import PageManager
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl

class MyCardMainFrameButtonBind:
    def __init__(self, master, frame):
        self.master = master
        self.my_card_main_frame = frame
        self.ui_frame_service = UiFrameServiceImpl.getInstance()
        self.page_manager = PageManager()

        self.deck_register_event_handler = CreateDeckRegisterScreen(self.my_card_main_frame)
        self.go_to_back_event_handler = GoToBackLobbyFrame(self.master, self.my_card_main_frame)
        self.create_decK_register_button_event_handler = CreateDeckRegisterButton(self.my_card_main_frame)
        self.next_page_screen_event_handler = NextPageScreen(self.my_card_main_frame, self.page_manager)
        self.previous_page_screen_event_handler = CreatePreviousPageScreen(self.my_card_main_frame, self.page_manager)

    def button_bind(self):
        print("마우스 클릭 이벤트들 바인드")
        self.my_card_main_frame.bind("<Button-1>", self.combined_mouse_click_event)

    def combined_mouse_click_event(self, event):
        self.deck_register_event_handler.mouse_click_event(event)
        self.go_to_back_event_handler.mouse_click_event(event)
        self.create_decK_register_button_event_handler.mouse_click_event(event)
        self.next_page_screen_event_handler.mouse_click_event(event)
        self.previous_page_screen_event_handler.mouse_click_event(event)