import tkinter

from battle_lobby_frame.entity.battle_lobby_frame import BattleLobbyFrame
from battle_lobby_frame.repository.battle_lobby_frame_repository import BattleLobbyFrameRepository
from utility.image_generator import ImageGenerator


class BattleLobbyFrameRepositoryImpl(BattleLobbyFrameRepository):
    __instance = None
    __decks = []
    __deckIds = []
    __currentDeckId = None
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

    def getCurrentDeckId(self):
        return self.__currentDeckId

    def addDeckToDeckList(self, deck):
        self.__decks.append(deck)

    def addDeckIdToDeckIdList(self, deckId):
        self.__deckIds.append(deckId)

    def selectDeck(self, deck):
        for i, d in enumerate(self.__decks):
            if d == deck:
                d.config(highlightthickness=5)
                self.__currentDeckId = self.__deckIds[i]
            else:
                d.config(highlightthickness=0)

    def requestCardList(self, RequestDeckCardList):
        if self.__currentDeckId is not None:
            print(f"self.__currentDeckId : {self.__currentDeckId}")
            self.__transmitIpcChannel.put(RequestDeckCardList)
            return self.__receiveIpcChannel.get()
        else:
            print('덱을 골라주세요!!')

    def exitBattleLobby(self):
        self.__currentDeckId = None
        for deck in self.__decks:
            deck.destroy()
        self.__decks.clear()
        self.__deckIds.clear()

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel
