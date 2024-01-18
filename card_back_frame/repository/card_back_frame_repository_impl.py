from card_back_frame.entity.card_back_frame import CardBackFrame
from card_back_frame.repository.card_back_frame_repository import CardBackFrameRepository


class CardBackFrameRepositoryImpl(CardBackFrameRepository):
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

    def createCardBackFrame(self, rootWindow):
        print("CardFrameRepositoryImpl: createCardFrame()")
        cardBackFrame = CardBackFrame(rootWindow)

        return cardBackFrame