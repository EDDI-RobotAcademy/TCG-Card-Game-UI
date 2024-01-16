from account_register_frame.entity.account_register_frame import AccountRegisterFrame
from account_register_frame.repository.account_register_frame_repository import AccountRegisterFrameRepository


class AccountRegisterFrameRepositoryImpl(AccountRegisterFrameRepository):
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

    def createAccountRegisterFrame(self, rootWindow):
        print("AccountRegisterFrameRepositoryImpl: createAccountRegisterFrame()")
        accountRegisterFrame = AccountRegisterFrame(rootWindow)

        return accountRegisterFrame

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("AccountRegisterFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("AccountRegisterFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestRegister(self, accountRegisterRequest):
        print(f"AccountRegisterFrameRepositoryImpl: requestRegister() -> {accountRegisterRequest}")
        self.__transmitIpcChannel.put(accountRegisterRequest)
        return self.__receiveIpcChannel.get()

