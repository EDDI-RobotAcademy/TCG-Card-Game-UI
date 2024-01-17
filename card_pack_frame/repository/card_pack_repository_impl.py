from card_pack_frame.entity.card_pack_frame import CardPackFrame
from card_pack_frame.repository.card_pack_repository import CardPackFrameRepository
from my_card_frame.entity.my_card_frame import MyCardFrame


class CardPackFrameRepositoryImpl(CardPackFrameRepository):
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

    def createCardPackFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createMainMenuFrame()")
        cardPackFrame = CardPackFrame(rootWindow)

        return cardPackFrame
