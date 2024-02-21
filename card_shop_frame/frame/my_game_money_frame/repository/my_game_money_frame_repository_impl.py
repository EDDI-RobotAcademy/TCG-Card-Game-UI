from card_shop_frame.frame.my_game_money_frame.entity.my_game_money_frame import MyGameMoneyFrame
from card_shop_frame.frame.my_game_money_frame.repository.my_game_money_frame_repository import MyGameMoneyFrameRepository


class MyGameMoneyFrameRepositoryImpl(MyGameMoneyFrameRepository):
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

    def createMyGameMoneyFrame(self, rootWindow):
        print("MyGameMoneyFrameRepositoryImpl: createMyGameMoneyFrame()")
        myGameMoneyFrame = MyGameMoneyFrame(rootWindow)

        return myGameMoneyFrame