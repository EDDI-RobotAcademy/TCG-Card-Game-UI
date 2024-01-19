from card.card_left_bottom_rendering.entity.card_left_bottom_rendering import CardLeftBottomRendering
from card.card_left_bottom_rendering.repository.card_left_bottom_rendering_repository import \
    CardLeftBottomRenderingRepository


class CardLeftBottomRenderingRepositoryImpl(CardLeftBottomRenderingRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardLeftBottomRenderingFrame(self, rootWindow):
        print("CardFrameRepositoryImpl: createCardFrame()")
        cardLeftBottomRendering = CardLeftBottomRendering(rootWindow)

        return cardLeftBottomRendering