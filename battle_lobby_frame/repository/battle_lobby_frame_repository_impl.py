import tkinter

from battle_lobby_frame.entity.battle_lobby_frame import BattleLobbyFrame
from battle_lobby_frame.repository.battle_lobby_frame_repository import BattleLobbyFrameRepository
from utility.image_generator import ImageGenerator


class BattleLobbyFrameRepositoryImpl(BattleLobbyFrameRepository):
    __instance = None
    __decks = []
    __currentDeckIndex = None
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

    def createBattleLobbyFrame(self, rootWindow):
        print("BattleLobbyFrameRepositoryImpl: createBattleLobbyFrame()")
        battleLobbyFrame = BattleLobbyFrame(rootWindow)

        return battleLobbyFrame

    def getDeckIndex(self):
        return self.__decks

    def getCurrentDeckIndex(self):
        return self.__currentDeckIndex

    def addDeckToDeckList(self, deck):
        self.__decks.append(deck)
        print(f"decks: {self.__decks}")


    def selectDeck(self, deck):
        for i, d in enumerate(self.__decks):
            if d == deck:
                d.config(highlightthickness=5)
                self.__currentDeckIndex = i
            else:
                d.config(highlightthickness=0)

    # TODO : 입장 버튼 클릭 시 실행 될 이벤트. 덱을 골랐을 때 호출 시 서버로 무작위 매칭을 요청합니다.
    def enterToRandomMatchingBattle(self, request):
        if self.__currentDeckIndex is not None:
            print(f"self.__currentDeckIndex : {self.__currentDeckIndex}")
            self.__transmitIpcChannel.put(request)
            return self.__receiveIpcChannel.get()
        else:
            print('덱을 골라주세요!!')

    def exitBattleLobby(self, switchFrameWithMenuName):
        self.__currentDeckIndex = None
        for deck in self.__decks:
            deck.destroy()
        self.__decks.clear()
        switchFrameWithMenuName('lobby-menu')

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel
