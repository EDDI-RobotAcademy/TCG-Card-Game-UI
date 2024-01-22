from card_random_frame.entity.card_random_frame import CardRandomFrame
from card_random_frame.repository.card_random_frame_repository import CardRandomFrameRepository


class CardRandomFrameRepositoryImpl(CardRandomFrameRepository):
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
        cardRandomFrame = CardRandomFrame(rootWindow)

        return cardRandomFrame