import tkinter

from card_back_frame.service.card_back_frame_service_impl import CardBackFrameServiceImpl
from card_merge_frame.repository.card_merge_frame_repository_impl import CardMergeFrameRepositoryImpl
from card_merge_frame.service.card_merge_frame_service import CardMergeFrameService


class CardMergeFrameServiceImpl(CardMergeFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardMergeFrameRepository = CardMergeFrameRepositoryImpl.getInstance()
            cls.__instance.__cardBackFrameService = CardBackFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardMergeUiFrame(self, rootWindow):
        CardMergeFrame = self.__cardMergeFrameRepository.createCardMergeFrame(rootWindow)

        CardBackFrame1 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame1.place(relx=0.15, rely=0.25, relwidth=0.20, relheight=0.43,anchor="center")

        CardBackFrame2 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame2.place(relx=0.38, rely=0.25, relwidth=0.20, relheight=0.43, anchor="center")

        CardBackFrame3 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame3.place(relx=0.61, rely=0.25, relwidth=0.20, relheight=0.43, anchor="center")

        CardBackFrame4 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame4.place(relx=0.84, rely=0.25, relwidth=0.20, relheight=0.43, anchor="center")

        CardBackFrame5 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame5.place(relx=0.15, rely=0.75, relwidth=0.20, relheight=0.43, anchor="center")

        CardBackFrame6 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame6.place(relx=0.38, rely=0.75, relwidth=0.20, relheight=0.43, anchor="center")

        CardBackFrame7 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame7.place(relx=0.61, rely=0.75, relwidth=0.20, relheight=0.43, anchor="center")

        CardBackFrame8 = self.__cardBackFrameService.createCardBackUiFrame(CardMergeFrame)
        CardBackFrame8.place(relx=0.84, rely=0.75, relwidth=0.20, relheight=0.43, anchor="center")

        return CardMergeFrame