from card.card_right_bottom_rendering.repository.card_right_bottom_rendering_repository_impl import \
    CardRightBottomRenderingRepositoryImpl
from card.card_right_bottom_rendering.service.card_right_bottom_rendering_service import CardRightBottomRenderingService


class CardRightBottomRenderingServiceImpl(CardRightBottomRenderingService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardRightBottomRenderingRepository = CardRightBottomRenderingRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardRightBottomRenderingUiFrame(self, rootWindow):
        cardRightBottomRendering = self.__cardRightBottomRenderingRepository.createCardRightBottomRenderingFrame(rootWindow)

        return cardRightBottomRendering
