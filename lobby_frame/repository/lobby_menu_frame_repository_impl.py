from lobby_frame.entity.lobby_menu_frame import LobbyMenuFrame
from lobby_frame.repository.lobby_menu_frame_repository import LobbyMenuFrameRepository


class LobbyMenuFrameRepositoryImpl(LobbyMenuFrameRepository):
    __instance = None
    __receiveIpcChannel = None
    __transmitIpcChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createLobbyMenuFrame(self, rootWindow):
        print("LobbyMenuFrameRepositoryImpl: createLobbyMenuFrame()")
        lobbyMenuFrame = LobbyMenuFrame(rootWindow)

        return lobbyMenuFrame


    def requestDeckNameList(self, deckNameRequest):
        self.__transmitIpcChannel.put(deckNameRequest)
        return self.__receiveIpcChannel.get()
        # return "테스트용 리턴값입니다."

    def requestProgramExit(self, exitRequest):
        self.__transmitIpcChannel.put(exitRequest)
        return self.__receiveIpcChannel.get()

    def requestAccountCardList(self, cardListRequest):
        self.__transmitIpcChannel.put(cardListRequest)
        return self.__receiveIpcChannel.get()

    def requestCheckGameMoney(self, CheckGameMoneyRequest):
        self.__transmitIpcChannel.put(CheckGameMoneyRequest)
        return self.__receiveIpcChannel.get()

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel

