import tkinter

from make_my_deck_frame.repository.make_my_deck_frame_repository_impl import MakeMyDeckFrameRepositoryImpl
from make_my_deck_frame.service.make_my_deck_frame_service import MakeMyDeckFrameService


class MakeMyDeckFrameServiceImpl(MakeMyDeckFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__makeMyDeckFrameRepository = MakeMyDeckFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMakeMyDeckUiFrame(self, rootWindow, switchFrameWithMenuName):
        makeMyDeckFrame = self.__makeMyDeckFrameRepository.createMakeMyDeckFrame(rootWindow)

        label_text = "덱 생성"
        label = tkinter.Label(makeMyDeckFrame, text=label_text, font=("Helvetica", 20), bg="#E18B6B", fg="black",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")


        go_back_to_lobby_button = tkinter.Button(makeMyDeckFrame, text="되돌아 가기", bg="#2E7D32", fg="white",
                                      command=lambda: switchFrameWithMenuName("my-card"), width=24, height=2)
        go_back_to_lobby_button.place(relx=0.3, rely=0.9, anchor="e")

        ok_button = tkinter.Button(makeMyDeckFrame, text="확인", bg="#C62828", fg="white",
                                     command=lambda: switchFrameWithMenuName("my-card"), width=24, height=2)
        ok_button.place(relx=0.7, rely=0.9, anchor="w")


        return makeMyDeckFrame