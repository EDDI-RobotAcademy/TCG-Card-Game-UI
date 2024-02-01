from matching_window.entity.matching_window_frame import MatchingWindowFrame
from matching_window.repository.matching_window_repository import MatchingWindowRepository


class MatchingWindowRepositoryImpl(MatchingWindowRepository):
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

    def createMatchingWindowFrame(self, rootWindow):
        matcingWindow = MatchingWindowFrame(rootWindow)
        return matcingWindow

    def cancelMatching(self, cancelMatchingRequest):
        self.__transmitIpcChannel.put(cancelMatchingRequest)
        return self.__receiveIpcChannel.get()
        # return "테스트용 리턴값입니다."

    def requestMatching(self, startMatchingRequest):
        self.__transmitIpcChannel.put(startMatchingRequest)
        return self.__receiveIpcChannel.get()

    def checkMatching(self, checkMatchingRequest):
        self.__transmitIpcChannel.put(checkMatchingRequest)
        return self.__receiveIpcChannel.get()

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel
