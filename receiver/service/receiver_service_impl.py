from receiver.repository.receiver_repository_impl import ReceiverRepositoryImpl
from receiver.service.receiver_service import ReceiverService


class ReceiverServiceImpl(ReceiverService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__receiverRepository = ReceiverRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def injectSocketClient(self, socketClient):
        print("ReceiverServiceImpl: injectSocketClient()")
        self.__receiverRepository.saveClientSocket(socketClient)

    def startToReceiveCommand(self):
        print("ReceiverServiceImpl: startToReceiveCommand()")
        self.__receiverRepository.receiveCommand()


