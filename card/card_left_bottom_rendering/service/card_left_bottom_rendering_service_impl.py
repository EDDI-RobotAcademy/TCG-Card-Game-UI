import tkinter

from card.card_left_bottom_rendering.repository.card_left_bottom_rendering_repository_impl import \
    CardLeftBottomRenderingRepositoryImpl
from card.card_left_bottom_rendering.service.card_left_bottom_rendering_service import CardLeftBottomRenderingService

class CardLeftBottomRenderingServiceImpl(CardLeftBottomRenderingService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardLeftBottomRenderingRepository = CardLeftBottomRenderingRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardLeftBottomRenderingUiFrame(self, rootWindow):
        cardLeftBottomRendering = self.__cardLeftBottomRenderingRepository.createCardLeftBottomRenderingFrame(rootWindow)

        return cardLeftBottomRendering
