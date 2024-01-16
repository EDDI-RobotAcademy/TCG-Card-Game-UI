import multiprocessing

from account_register_frame.service.account_register_frame_service_impl import AccountRegisterFrameServiceImpl
from app_window.service.window_service_impl import WindowServiceImpl
from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from account_login_frame.service.login_menu_frame_service_impl import LoginMenuFrameServiceImpl
from main_frame.service.main_menu_frame_service_impl import MainMenuFrameServiceImpl
from receiver.controller.receiver_controller_impl import ReceiverControllerImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.controller.transmitter_controller_impl import TransmitterControllerImpl
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl


class DomainInitializer:
    # UI Frame
    @staticmethod
    def initRootWindowDomain():
        WindowServiceImpl.getInstance()

    @staticmethod
    def initMainMenuFrameDomain():
        MainMenuFrameServiceImpl.getInstance()

    @staticmethod
    def initLoginMenuFrameDomain():
        LoginMenuFrameServiceImpl.getInstance()

    @staticmethod
    def initUiFrameDomain(uiTransmitIpcChannel):
        uiFrameController = UiFrameControllerImpl.getInstance()
        uiFrameController.requestToInjectTransmitIpcChannel(uiTransmitIpcChannel)

    @staticmethod
    def initAccountRegisterFrameDomain():
        AccountRegisterFrameServiceImpl.getInstance()

    # Socket Domain
    @staticmethod
    def initClientSocketDomain():
        ClientSocketServiceImpl.getInstance()

    @staticmethod
    def initTransmitterDomain(uiTransmitIpcChannel):
        transmitterController = TransmitterControllerImpl.getInstance()
        transmitterController.requestToInjectUiIpcChannel(uiTransmitIpcChannel)

    @staticmethod
    def initReceiverDomain(uiReceiveIpcChannel):
        receiverController = ReceiverControllerImpl.getInstance()
        receiverController.requestToInjectUiIpcChannel(uiReceiveIpcChannel)

    # Task Worker Domain
    @staticmethod
    def initTaskWorkerDomain():
        TaskWorkerServiceImpl.getInstance()

    @staticmethod
    def initEachDomain():
        # IPC Channel
        uiTransmitIpcChannel = multiprocessing.Queue()
        uiReceiveIpcChannel = multiprocessing.Queue

        # UI Frame Domain
        DomainInitializer.initRootWindowDomain()
        DomainInitializer.initMainMenuFrameDomain()
        DomainInitializer.initLoginMenuFrameDomain()
        DomainInitializer.initAccountRegisterFrameDomain()
        DomainInitializer.initUiFrameDomain(uiTransmitIpcChannel)

        # Socket Domain
        DomainInitializer.initClientSocketDomain()
        DomainInitializer.initTransmitterDomain(uiTransmitIpcChannel)
        DomainInitializer.initReceiverDomain(uiReceiveIpcChannel)

        # Task Worker Domain
        DomainInitializer.initTaskWorkerDomain()








