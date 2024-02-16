import tkinter

from tests.ljl.my_card_frame_legacy.repository.my_card_frame_repository_impl import MyCardFrameRepositoryImpl
from tests.ljl.my_card_frame_legacy.service.my_card_frame_service import MyCardFrameService
from card_merge_frame.service.card_merge_frame_service_impl import CardMergeFrameServiceImpl


class MyCardFrameServiceImpl(MyCardFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myCardFrameRepository = MyCardFrameRepositoryImpl.getInstance()
            cls.__instance.__cardMergeFrameService = CardMergeFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        myCardFrame = self.__myCardFrameRepository.createMyCardFrame(rootWindow)

        label_text = "My Card"
        label = tkinter.Label(myCardFrame, text=label_text, font=("Helvetica", 20), bg="#AE905E", fg="black",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")


        CardMergeFrame = self.__cardMergeFrameService.createCardMergeUiFrame(myCardFrame)
        CardMergeFrame.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.63, anchor="center")


        return myCardFrame