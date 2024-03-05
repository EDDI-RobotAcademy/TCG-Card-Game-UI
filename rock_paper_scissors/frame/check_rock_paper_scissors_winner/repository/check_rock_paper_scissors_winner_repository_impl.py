from rock_paper_scissors.frame.check_rock_paper_scissors_winner.entity.check_rock_paper_scissors_winner import CheckRockPaperScissorsWinnerFrame
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.repository.check_rock_paper_scissors_winner_repository import CheckRockPaperScissorsWinnerRepository


class CheckRockPaperScissorsWinnerRepositoryImpl(CheckRockPaperScissorsWinnerRepository):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None
    __RPSWinner = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCheckRockPaperScissorsWinnerFrame(self, rootWindow):
        print("CheckRockPaperScissorsWinnerRepositoryImpl: createCheckRockPaperScissorsWinnerFrame()")
        checkRockPaperScissorsWinnerFrame = CheckRockPaperScissorsWinnerFrame(rootWindow)

        return checkRockPaperScissorsWinnerFrame

    def requestCheckRockPaperScissorsWinner(self, CheckRockPaperScissorsWinnerRequest):
        print(f"CheckRockPaperScissorsWinnerRepositoryImpl: requestCheckRockPaperScissorsWinner() -> {CheckRockPaperScissorsWinnerRequest}")
        self.__transmitIpcChannel.put(CheckRockPaperScissorsWinnerRequest)
        return self.__receiveIpcChannel.get()


    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("CheckRockPaperScissorsWinnerRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("CheckRockPaperScissorsWinnerRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def setRPSWinner(self, RPSWinner):
        print("CheckRockPaperScissorsWinnerRepositoryImpl: setRPSWinner()")
        self.__RPSWinner = RPSWinner
        print(f"{self.__RPSWinner}")

    def getRPSWinner(self):
        print("CheckRockPaperScissorsWinnerRepositoryImpl: getRPSWinner()")
        return self.__RPSWinner
