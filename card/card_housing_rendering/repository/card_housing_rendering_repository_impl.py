from card.card_housing_rendering.entity.card_housing_rendering_entity import CardHousingRendering
from card.card_housing_rendering.repository.card_housing_rendering_repository import CardHousingRenderingRepository


class CardHousingRenderingRepositoryImpl(CardHousingRenderingRepository):
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

    def createCardHousingRendering(self, rootWindow):
        print("CardFrameRepositoryImpl: createCardFrame()")
        cardFrame = CardHousingRendering(rootWindow)

        return cardFrame