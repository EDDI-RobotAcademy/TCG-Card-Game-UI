from rock_paper_scissors.entity.rock_paper_scissors import RockPaperScissors
from rock_paper_scissors.repository.rock_paper_scissors_repository import RockPaperScissorsRepository


class RockPaperScissorsRepositoryImpl(RockPaperScissorsRepository):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None

    def __init__(self):
        self.__rps = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createRockPaperScissorsFrame(self, rootWindow):
        print("RockPaperScissorsRepositoryImpl: createMainMenuFrame()")
        cardShopMenuFrame = CardShopMenuFrame(rootWindow)

        return cardShopMenuFrame

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("RockPaperScissorsRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("RockPaperScissorsRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel


    def setRPS(self, rps):
        print(f"CardShopFrameRepositoryImpl rps set {rps}")
        self.__rps = rps

    def getRPS(self):
        return self.__rps
