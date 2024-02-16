from card_shop_frame.entity.card_shop_menu_frame import CardShopMenuFrame
from card_shop_frame.repository.card_shop_repository import CardShopMenuFrameRepository


class CardShopMenuFrameRepositoryImpl(CardShopMenuFrameRepository):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None

    def __init__(self):
        self.__race = None

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

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("CardShopFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("CardShopFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestCheckGameMoney(self, CheckGameMoneyRequest):
        print(f"CardShopFrameRepositoryImpl: requestCheckGameMoney() -> {CheckGameMoneyRequest}")
        self.__transmitIpcChannel.put(CheckGameMoneyRequest)
        return self.__receiveIpcChannel.get()

    def setRace(self, race):
        print(f"CardShopFrameRepositoryImpl race set {race}")
        self.__race = race

    def getRace(self):
        return self.__race
