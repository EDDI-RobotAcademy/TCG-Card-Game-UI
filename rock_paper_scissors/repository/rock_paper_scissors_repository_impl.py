from rock_paper_scissors.entity.rock_paper_scissors import RockPaperScissorsFrame
from rock_paper_scissors.repository.rock_paper_scissors_repository import RockPaperScissorsRepository


class RockPaperScissorsRepositoryImpl(RockPaperScissorsRepository):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None

    def __init__(self):
        self.__rps = ""
        self.__RPS_timer_click = False
        self.__checkRPS = False
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
        rockPaperScissorsFrame = RockPaperScissorsFrame(rootWindow)

        return rockPaperScissorsFrame

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("RockPaperScissorsRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("RockPaperScissorsRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def setRPS(self, rps):
        print(f"RockPaperScissorsRepositoryImpl rps set {rps}")
        self.__rps = rps

    def getRPS(self):
        return self.__rps

    def resetRPS(self):
        self.__rps = ""


    def setRPSTimerClick(self, checkClick):
        print(f"RockPaperScissorsRepositoryImpl rps checkClick {checkClick}")
        self.__RPS_timer_click = checkClick

    def getRPSTimerClick(self):
        return self.__RPS_timer_click

    def requestRockPaperScissors(self, RockPaperScissorsRequest):
        print(f"RockPaperScissorsRepositoryImpl: requestRockPaperScissors() -> {RockPaperScissorsRequest}")
        self.__transmitIpcChannel.put(RockPaperScissorsRequest)
        return self.__receiveIpcChannel.get()

    def requestCheckRockPaperScissorsWinner(self, CheckRockPaperScissorsWinnerRequest):
        print(f"RockPaperScissorsRepositoryImpl: requestCheckRockPaperScissorsWinner() -> {CheckRockPaperScissorsWinnerRequest}")
        self.__transmitIpcChannel.put(CheckRockPaperScissorsWinnerRequest)
        return self.__receiveIpcChannel.get()
