from card_shop_frame.frame.buy_check_frame.entity.buy_check_frame import BuyCheckFrame
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository import BuyCheckRepository


class BuyCheckRepositoryImpl(BuyCheckRepository):
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

    def createBuyCheckFrame(self, rootWindow):
        print("BuyCheckRepositoryImpl: createBuyCheckFrame()")
        buyCheckFrame = BuyCheckFrame(rootWindow)

        return buyCheckFrame

    def destroyBuyCheckFrame(self, rootWindow):
        print("BuyCheckRepositoryImpl: destroyBuyCheckFrame()")
        buyCheckFrame = BuyCheckFrame.destroy(rootWindow)
        return buyCheckFrame