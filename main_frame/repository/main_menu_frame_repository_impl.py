from main_frame.entity.main_menu_frame import MainMenuFrame
from main_frame.repository.main_menu_frame_repository import MainMenuFrameRepository


class MainMenuFrameRepositoryImpl(MainMenuFrameRepository):
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

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("MainMenuFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("MainMenuFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def createMainMenuFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createMainMenuFrame()")
        mainMenuFrame = MainMenuFrame(rootWindow)

        return mainMenuFrame

    def requestProgramExit(self, programExitRequest):
        print("MainMenuFrameRepositoryImpl: requestProgramExit()")

        self.__transmitIpcChannel.put(programExitRequest)
        return self.__receiveIpcChannel.get()





