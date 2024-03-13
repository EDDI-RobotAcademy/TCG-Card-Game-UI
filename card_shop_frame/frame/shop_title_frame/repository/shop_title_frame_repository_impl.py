from card_shop_frame.frame.shop_title_frame.entity.shop_title_frame import ShopTitleFrame
from card_shop_frame.frame.shop_title_frame.repository.shop_title_frame_repository import ShopTitleFrameRepository


class ShopTitleFrameRepositoryImpl(ShopTitleFrameRepository):
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

    def createShopTitleFrame(self, rootWindow):
        print("ShopTitleFrameRepositoryImpl: createShopTitleFrame()")
        shopTitleFrame = ShopTitleFrame(rootWindow)

        return shopTitleFrame
