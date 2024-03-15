from card_shop_frame.frame.select_race_ui_frame.entity.select_race_ui_frame import SelectRaceUiFrame
from card_shop_frame.frame.select_race_ui_frame.repository.select_race_ui_frame_repository import SelectRaceUiFrameRepository


class SelectRaceUiFrameRepositoryImpl(SelectRaceUiFrameRepository):
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

    def createSelectRaceUiFrame(self, rootWindow):
        print("BuyCheckRepositoryImpl: createSelectRaceUiFrame()")
        selectRaceUiFrame = SelectRaceUiFrame(rootWindow)

        return selectRaceUiFrame

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
