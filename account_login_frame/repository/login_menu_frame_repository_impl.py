from tkinter import ttk, CENTER

from account_login_frame.entity.login_menu_frame import LoginMenuFrame
from account_login_frame.repository.login_menu_frame_repository import LoginMenuFrameRepository


class LoginMenuFrameRepositoryImpl(LoginMenuFrameRepository):
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

    def createLoginMenuFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createMainMenuFrame()")
        loginMenuFrame = LoginMenuFrame(rootWindow)

        return loginMenuFrame

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("MainMenuFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("MainMenuFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestLogin(self, accountLoginRequest):
        print(f"MainMenuFrameRepositoryImpl: requestLogin() -> {accountLoginRequest}")

        self.__transmitIpcChannel.put(accountLoginRequest)
        return self.__receiveIpcChannel.get()



