import unittest

import colorama

from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_frame_service_impl import BattleLobbyFrameServiceImpl
from battle_lobby_frame.service.request.request_deck_card_list import RequestDeckCardList
from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from initializer.init_domain import DomainInitializer
from receiver.controller.receiver_controller_impl import ReceiverControllerImpl
from session.repository.session_repository_impl import SessionRepositoryImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.controller.transmitter_controller_impl import TransmitterControllerImpl


class TestUglyBattleLobby(unittest.TestCase):
    def setUp(self):
        DomainInitializer.initEachDomain()
        colorama.init(autoreset=True)

        clientSocketService = ClientSocketServiceImpl.getInstance()
        clientSocket = clientSocketService.createClientSocket()
        clientSocketService.connectToTargetHost()

        transmitterController = TransmitterControllerImpl.getInstance()
        transmitterController.requestToInjectSocketClient(clientSocket)

        receiverController = ReceiverControllerImpl.getInstance()
        receiverController.requestToInjectSocketClient(clientSocket)

        taskWorkerService = TaskWorkerServiceImpl.getInstance()

        taskWorkerService.createTaskWorker("Transmitter", transmitterController.requestToTransmitCommand)
        taskWorkerService.executeTaskWorker("Transmitter")

        taskWorkerService.createTaskWorker("Receiver", receiverController.requestToReceiveCommand)
        taskWorkerService.executeTaskWorker("Receiver")


    def test_battle_lobby_service_impl(self):
        __battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
        __battleLobbyFrameService = BattleLobbyFrameServiceImpl.getInstance()
        __sessionRepository = SessionRepositoryImpl.getInstance()

        # self.__battleLobbyFrameService.createBattleLobbyMyDeckButton(requestData)

        # self.__battleLobbyFrameService.checkTimeForDeckSelection(battleLobbyFrame)
        response = __battleLobbyFrameRepository.requestCardList(
            RequestDeckCardList(2,
                                "eab86cd4-8d5d-492c-81b4-cc53118cd401")
        )
        self.assertIsNotNone(response)
        #print(response)

if __name__ == '__main__':
    unittest.main()
