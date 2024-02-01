from tkinter import ttk

from opengl_my_card_main_frame_legacy.frame.my_card_main_frame import MyCardMainFrame
from opengl_my_card_main_frame_legacy.service.my_card_main_frame_service import MyCardMainFrameService


class MyCardMainFrameServiceImpl(MyCardMainFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myCardMainFrame = MyCardMainFrame
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyCardMainUiFrame(self, rootWindow, switchFrameWithMenuName):
        myCardMainFrame = self.__myCardMainFrame(rootWindow)

        style = ttk.Style()
        style.configure("TFrame", background="#DEB852")
        style.configure("TLabel", background="#DEB852", foreground="#ffffff", font=("Arial", 30))
        style.configure("TButton", background="#2C3E50", foreground="#ffffff", font=("Arial", 12), padding=(10, 5))

        label_myCardMainText = ttk.Label(myCardMainFrame, text="My Card", style="TLabel")

        button_create_deck = ttk.Button(myCardMainFrame, text="덱 생성", style="TButton")
        button_go_back_to_lobby = ttk.Button(myCardMainFrame, text="로비로 돌아가기", style="TButton")

        def on_deck_register_click(event):
            try:
                if event.widget == button_create_deck:
                    myCardMainFrame.toggle_visibility()
                    #switchFrameWithMenuName("my-deck-register")

                elif event.widget == button_go_back_to_lobby:
                    switchFrameWithMenuName("lobby-menu")

            except Exception as e:
                print(f"An error occurred: {e}")

        # 버튼 클릭 시 호출되는 함수 설정
        button_create_deck.bind("<Button-1>", on_deck_register_click)
        button_go_back_to_lobby.bind("<Button-1>", on_deck_register_click)

        label_myCardMainText.place(relx=0.5, rely=0.2, anchor="center")
        button_create_deck.place(relx=0.85, rely=0.8, anchor="center")
        button_go_back_to_lobby.place(relx=0.85, rely=0.9, anchor="center")


        return myCardMainFrame