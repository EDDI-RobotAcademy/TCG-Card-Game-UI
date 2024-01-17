from card_frame.entity.card_frame import CardFrame
from card_frame.repository.card_frame_repository import CardFrameRepository


class CardFrameRepositoryImpl(CardFrameRepository):
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

    def createCardFrame(self, rootWindow):
        print("CardFrameRepositoryImpl: createCardFrame()")
        cardFrame = CardFrame(rootWindow)

        return cardFrame