from transmitter.controller.transmitter_controller import TransmitterController
from transmitter.service.transmitter_service_impl import TransmitterServiceImpl


class TransmitterControllerImpl(TransmitterController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__transmitterService = TransmitterServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestToInjectSocketClient(self, socketClient):
        print("TransmitterControllerImpl: requestToInjectSocketClient()")
        self.__transmitterService.injectSocketClient(socketClient)








