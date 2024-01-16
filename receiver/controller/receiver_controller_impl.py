from receiver.controller.receiver_controller import ReceiverController
from receiver.service.receiver_service_impl import ReceiverServiceImpl


class ReceiverControllerImpl(ReceiverController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__receiverService = ReceiverServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestToInjectSocketClient(self, socketClient):
        print("ReceiverControllerImpl: requestToInjectSocketClient()")
        self.__receiverService.injectSocketClient(socketClient)

    def requestToInjectUiIpcChannel(self, uiIpcChannel):
        print("ReceiverControllerImpl: requestToInjectIpcChannel()")
        self.__receiverService.injectUiIpcChannel(uiIpcChannel)

    def requestToReceiveCommand(self):
        print("ReceiverControllerImpl: requestToReceiveCommand()")
        self.__receiverService.startToReceiveCommand()




