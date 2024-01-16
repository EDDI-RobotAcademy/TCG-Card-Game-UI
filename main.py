import colorama

from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from initializer.init_domain import DomainInitializer
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

    uiFrameController = UiFrameControllerImpl.getInstance()
    uiFrameController.requestToCreateUiFrame()

    taskWorkerService = TaskWorkerServiceImpl.getInstance()
    taskWorkerService.createTaskWorker("Transmitter", transmitterController.requestToTransmitCommand)
    taskWorkerService.executeTaskWorker("Transmitter")

    taskWorkerService.createTaskWorker("Receiver", receiverController.requestToReceiveCommand)
    taskWorkerService.executeTaskWorker("Receiver")

    taskWorkerService.createTaskWorker("UI", uiFrameController.requestToStartPrintGameUi)
    taskWorkerService.executeTaskWorker("UI")

