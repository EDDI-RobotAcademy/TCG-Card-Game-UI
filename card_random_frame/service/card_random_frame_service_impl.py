import tkinter

from card_random_frame.repository.card_random_frame_repository_impl import CardRandomFrameRepositoryImpl
from card_random_frame.service.card_random_frame_service import CardRandomFrameService


class CardRandomFrameServiceImpl(CardRandomFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardRandomFrameRepository = CardRandomFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardRandomUiFrame(self, rootWindow, switchFrameWithMenuName):
        CardRandomFrame = self.__cardRandomFrameRepository.createCardRandomFrame(rootWindow)

        


        return CardRandomFrame