from card.card_right_up_rendering.repository.card_right_up_rendering_repository_impl import \
    CardRightUpRenderingRepositoryImpl
from card.card_right_up_rendering.service.card_right_up_rendering_service import CardRightUpRenderingService


class CardRightUpRenderingServiceImpl(CardRightUpRenderingService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardRightUpRenderingRepository = CardRightUpRenderingRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardRightUpRenderingUiFrame(self, rootWindow):
        cardRightUpRendering = self.__cardRightUpRenderingRepository.createCardRightUpRenderingFrame(rootWindow)

        return cardRightUpRendering
