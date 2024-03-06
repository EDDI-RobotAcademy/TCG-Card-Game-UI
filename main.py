import colorama

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from initializer.init_domain import DomainInitializer
from music_player.controller.music_player_controller_impl import MusicPlayerControllerImpl
from notify_reader.controller.notify_reader_controller_impl import NotifyReaderControllerImpl
from receiver.controller.receiver_controller_impl import ReceiverControllerImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.controller.transmitter_controller_impl import TransmitterControllerImpl
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl


DomainInitializer.initEachDomain()



if __name__ == "__main__":
    # Console Color
    colorama.init(autoreset=True)

    clientSocketService = ClientSocketServiceImpl.getInstance()
    clientSocket = clientSocketService.createClientSocket()
    clientSocketService.connectToTargetHost()

    transmitterController = TransmitterControllerImpl.getInstance()
    transmitterController.requestToInjectSocketClient(clientSocket)

    receiverController = ReceiverControllerImpl.getInstance()
    receiverController.requestToInjectSocketClient(clientSocket)
    #
    # notifyReaderController = NotifyReaderControllerImpl.getInstance()
    # notifyReaderController.requestToMappingNoticeWithFunction()

    uiFrameController = UiFrameControllerImpl.getInstance()
    uiFrameController.requestToCreateUiFrame()
    uiFrameController.first_main_window()

    musicPlayerController = MusicPlayerControllerImpl.getInstance()
    musicPlayerController.loadAllMusicFiles()

    taskWorkerService = TaskWorkerServiceImpl.getInstance()
    taskWorkerService.createTaskWorker("Transmitter", transmitterController.requestToTransmitCommand)
    taskWorkerService.executeTaskWorker("Transmitter")

    taskWorkerService.createTaskWorker("Receiver", receiverController.requestToReceiveCommand)
    taskWorkerService.executeTaskWorker("Receiver")
    #
    # taskWorkerService.createTaskWorker("NotifyReader", notifyReaderController.requestToReadNotifyCommand)
    # taskWorkerService.executeTaskWorker("NotifyReader")

    taskWorkerService.createTaskWorker("UI", uiFrameController.requestToStartPrintGameUi)
    taskWorkerService.executeTaskWorker("UI")

    # uiFrameController.register_fake_battle_field_frame_which_one_has_socket_communication()

    # taskWorkerService.createTaskWorker("MusicPlayer", musicPlayerController.playBackgroundMusic)
    # taskWorkerService.executeTaskWorker("MusicPlayer")
