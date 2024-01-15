from card_shop_frame.entity.card_shop_menu_frame import CardShopMenuFrame
from card_shop_frame.repository.card_shop_repository import CardShopMenuFrameRepository


class CardShopMenuFrameRepositoryImpl(CardShopMenuFrameRepository):
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

    def createCardShopMenuFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createMainMenuFrame()")
        cardShopMenuFrame = CardShopMenuFrame(rootWindow)

        return cardShopMenuFrame

