from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from initializer.init_domain import DomainInitializer
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.controller.transmitter_controller_impl import TransmitterControllerImpl
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl


DomainInitializer.initEachDomain()


if __name__ == "__main__":
    clientSocketService = ClientSocketServiceImpl.getInstance()
    clientSocket = clientSocketService.createClientSocket()
    clientSocketService.connectToTargetHost()

    transmitterController = TransmitterControllerImpl.getInstance()
    transmitterController.requestToInjectSocketClient(clientSocket)

    uiFrameController = UiFrameControllerImpl.getInstance()
    uiFrameController.requestToCreateUiFrame()

    taskWorkerService = TaskWorkerServiceImpl.getInstance()
    taskWorkerService.createTaskWorker("UI", uiFrameController.requestToStartPrintGameUi)
    taskWorkerService.executeTaskWorker("UI")


