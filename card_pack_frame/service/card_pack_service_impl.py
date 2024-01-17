import tkinter

from card_pack_frame.repository.card_pack_repository_impl import CardPackFrameRepositoryImpl
from card_pack_frame.service.card_pack_service import CardPackFrameService


class CardPackFrameServiceImpl(CardPackFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardPackFrameRepository = CardPackFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def createCardPackUiFrame(self, rootWindow):
        cardPackFrame = self.__cardPackFrameRepository.createCardPackFrame(rootWindow)

        return cardPackFrame
