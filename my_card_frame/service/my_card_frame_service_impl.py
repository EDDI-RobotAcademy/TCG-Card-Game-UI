import tkinter

from my_card_frame.repository.my_card_frame_repository_impl import MyCardFrameRepositoryImpl
from my_card_frame.service.my_card_frame_service import MyCardFrameService


class MyCardFrameServiceImpl(MyCardFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myCardFrameRepository = MyCardFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        myCardFrame = self.__myCardFrameRepository.createMyCardFrame(rootWindow)

        label_text = "This is my card frame"
        label = tkinter.Label(myCardFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬

        deck_generation_button = tkinter.Button(myCardFrame, text="덱 생성", bg="#2E7D32", fg="white",
                                      command=lambda: switchFrameWithMenuName("lobby-menu"), width=24, height=2)
        deck_generation_button.place(relx=0.8, rely=0.8, anchor="center")

        go_back_to_lobby_button = tkinter.Button(myCardFrame, text="로비로 돌아가기", bg="#C62828", fg="white",
                                     command=lambda: switchFrameWithMenuName("lobby-menu"), width=24, height=2)
        go_back_to_lobby_button.place(relx=0.8, rely=0.9, anchor="center")

        return myCardFrame
