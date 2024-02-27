from card_shop_frame.frame.buy_check_frame.entity.buy_check_frame import BuyCheckFrame
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository import BuyCheckRepository


class BuyCheckRepositoryImpl(BuyCheckRepository):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None
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

    def createBuyCheckFrame(self, rootWindow):
        print("BuyCheckRepositoryImpl: createBuyCheckFrame()")
        buyCheckFrame = BuyCheckFrame(rootWindow)

        return buyCheckFrame

    def requestUseGameMoney(self, UseGameMoneyRequest):
        print(f"BuyCheckRepositoryImpl: requestCheckGameMoney() -> {UseGameMoneyRequest}")
        self.__transmitIpcChannel.put(UseGameMoneyRequest)
        return self.__receiveIpcChannel.get()

    def requestBuyRandomCard(self, buyRandomCardRequest):
        print(f"BuyCheckRepositoryImpl: requestBuyRandomCard() -> {buyRandomCardRequest}")

        self.__transmitIpcChannel.put(buyRandomCardRequest)
        return self.__receiveIpcChannel.get()

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("BuyCheckRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("BuyCheckRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def setRandomCardList(self, randomCardList):
        print("BuyCheckRepositoryImpl: setRandomCardList()")
        self.__randomCardList = randomCardList
        print(f"{self.__randomCardList}")

    def getRandomCardList(self):
        print("BuyCheckRepositoryImpl: getRandomCardList()")
        return self.__randomCardList
