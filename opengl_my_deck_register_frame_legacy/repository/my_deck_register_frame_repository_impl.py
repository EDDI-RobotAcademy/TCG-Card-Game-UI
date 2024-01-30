from opengl_my_deck_register_frame_legacy.repository.my_deck_register_frame_repository import \
    MyDeckRegisterFrameRepository

class MyDeckRegisterFrameRepositoryImpl(MyDeckRegisterFrameRepository):
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
        print("MyDeckRegisterFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("MyDeckRegisterFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestRegister(self, myDeckRegisterRequest):
        print(f"MyDeckRegisterFrameRepositoryImpl: requestRegister() -> {myDeckRegisterRequest}")
        self.__transmitIpcChannel.put(myDeckRegisterRequest)
        return self.__receiveIpcChannel.get()