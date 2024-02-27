from buy_random_card_frame_legacy.entity.buy_random_card_frame import BuyRandomCardFrame
from buy_random_card_frame_legacy.repository.buy_random_card_frame_repository import BuyRandomCardFrameRepository


class BuyRandomCardFrameRepositoryImpl(BuyRandomCardFrameRepository):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBuyRandomCardFrame(self, rootWindow):
        print("BuyRandomCardFrameRepositoryImpl: createBuyRandomCardFrame()")
        buyRandomCardFrame = BuyRandomCardFrame(rootWindow)

        return buyRandomCardFrame

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("BuyRandomCardFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("BuyRandomCardFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestBuyRandomCard(self, buyRandomCardRequest):
        print(f"BuyRandomCardFrameRepositoryImpl: requestBuyRandomCard() -> {buyRandomCardRequest}")

        self.__transmitIpcChannel.put(buyRandomCardRequest)
        return self.__receiveIpcChannel.get()
