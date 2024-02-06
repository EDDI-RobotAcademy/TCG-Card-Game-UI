from tkinter import ttk
import tkinter as tk

from button.buntton_handler.button_handler_impl import ButtonHandlerImpl
from common.button_type import ButtonType
from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.frame.my_card_main_frame import MyCardMainFrame
from opengl_my_card_main_frame.service.my_card_main_frame_service import MyCardMainFrameService


class MyCardMainFrameServiceImpl(MyCardMainFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myCardMainFrame = MyCardMainFrame
            cls.__instance.__myCardMainScene = MyCardMainScene()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyCardMainUiFrame(self, rootWindow, switchFrameWithMenuName):
        myCardMainFrame = self.__myCardMainFrame(rootWindow)

        # ButtonHandlerImpl()
        # button_handler = ButtonHandlerImpl.getInstance()
        #
        # buttonFunction = button_handler.getButtonTypeTable(ButtonType.DECKREGISTER.value)
        # buttonFunction(rootWindow, myCardMainFrame.getCanvas(), myCardMainFrame.make_my_deck_register_frame())
        # button_handler.getButtonTypeTable(2)




        # button_create_deck = tk.Button(myCardMainFrame, text="덱 생성", fg="white", bg="#483C32", width=25, height=2)
        # button_go_back_to_lobby = tk.Button(myCardMainFrame, text="로비로 돌아가기", fg="white", bg="#483C32", width=25, height=2)
        #
        # def on_deck_create_click(event):
        #     try:
        #         if event.widget == button_create_deck:
        #             myCardMainFrame.toggle_visibility()
        #
        #         elif event.widget == button_go_back_to_lobby:
        #             switchFrameWithMenuName("lobby-menu")
        #
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        #
        # # 버튼 클릭 시 호출되는 함수 설정
        # button_create_deck.bind("<Button-1>", on_deck_create_click)
        # button_go_back_to_lobby.bind("<Button-1>", on_deck_create_click)
        #
        # button_create_deck.place(relx=0.88, rely=0.80, anchor="center")
        # button_go_back_to_lobby.place(relx=0.88, rely=0.90, anchor="center")


        return myCardMainFrame

    def button_bind(self, button_list):
        button_create_deck = button_list[0]
        button_go_back_to_lobby = button_list[1]
        button_create_deck.bind("<Button-1>", self.__myCardMainFrame.toggle_visibility())
