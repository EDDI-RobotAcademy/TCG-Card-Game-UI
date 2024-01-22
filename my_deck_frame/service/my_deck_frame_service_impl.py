import tkinter

from my_deck_frame.repository.my_deck_frame_repository_impl import MyDeckFrameRepositoryImpl
from my_deck_frame.service.my_deck_frame_service import MyDeckFrameService
from transparent_background_frame.repository.transparent_background_frame_repository_impl import \
    TransparentBackgroundFrameRepositoryImpl


class MyDeckFrameServiceImpl(MyDeckFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myDeckFrameRepository = MyDeckFrameRepositoryImpl.getInstance()
            cls.__instance.__transparentBackgroundFrameRepository = TransparentBackgroundFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyDeckUiFrame(self, rootWindow, switchFrameWithMenuName):
        myDeckFrame = self.__myDeckFrameRepository.createMyDeckFrame(rootWindow)

        label_text = "나의 덱"
        label = tkinter.Label(myDeckFrame, text=label_text, font=("Helvetica", 15), bg="#D7AC87", fg="black",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")

        deck_generation_button = tkinter.Button(myDeckFrame, text="덱 생성", bg="#2E7D32", fg="white",
                                      command=lambda: switchFrameWithMenuName("my-card"), width=24, height=2)
        deck_generation_button.place(relx=0.5, rely=0.8, anchor="center")

        go_back_to_lobby_button = tkinter.Button(myDeckFrame, text="로비로 돌아가기", bg="#C62828", fg="white",
                                     command=lambda: switchFrameWithMenuName("lobby-menu"), width=24, height=2)
        go_back_to_lobby_button.place(relx=0.5, rely=0.9, anchor="center")


        return myDeckFrame