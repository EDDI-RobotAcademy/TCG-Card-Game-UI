from card_shop_frame.frame.shop_button_frame.entity.shop_button_frame import ShopButtonFrame
from card_shop_frame.frame.shop_button_frame.repository.shop_button_frame_repository import ShopButtonFrameRepository


class ShopButtonFrameRepositoryImpl(ShopButtonFrameRepository):
    __instance = None
    __randomCardList = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createShopButtonFrame(self, rootWindow):
        print("ShopButtonRepositoryImpl: createShopButtonFrame()")
        shopButtonFrame = ShopButtonFrame(rootWindow)

        return shopButtonFrame

    def setRandomCardList(self, randomCardList):
        print("ShopButtonRepositoryImpl: setRandomCardList()")
        self.__randomCardList = randomCardList
        print(f"{self.__randomCardList}")

    def getRandomCardList(self):
        print("ShopButtonRepositoryImpl: getRandomCardList()")
        return self.__randomCardList
