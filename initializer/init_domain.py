from account_register_frame.service.account_register_frame_service_impl import AccountRegisterFrameServiceImpl
from app_window.service.window_service_impl import WindowServiceImpl
from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from login_frame.service.login_menu_frame_service_impl import LoginMenuFrameServiceImpl
from main_frame.service.main_menu_frame_service_impl import MainMenuFrameServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.controller.transmitter_controller_impl import TransmitterControllerImpl
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl


class DomainInitializer:

    @staticmethod
    def initRootWindowDomain():
        WindowServiceImpl.getInstance()

    @staticmethod
    def initTaskWorkerDomain():
        TaskWorkerServiceImpl.getInstance()

    @staticmethod
    def initMainMenuFrameDomain():
        MainMenuFrameServiceImpl.getInstance()

    @staticmethod
    def initLoginMenuFrameDomain():
        LoginMenuFrameServiceImpl.getInstance()

    @staticmethod
    def initTransmitterDomain():
        TransmitterControllerImpl.getInstance()

    @staticmethod
    def initClientSocketDomain():
        ClientSocketServiceImpl.getInstance()

    @staticmethod
    def initUiFrameDomain():
        UiFrameControllerImpl.getInstance()

    @staticmethod
    def initAccountRegisterFrameDomain():
        AccountRegisterFrameServiceImpl.getInstance()

    @staticmethod
    def initEachDomain():
        DomainInitializer.initRootWindowDomain()
        DomainInitializer.initMainMenuFrameDomain()
        DomainInitializer.initLoginMenuFrameDomain()
        DomainInitializer.initAccountRegisterFrameDomain()
        DomainInitializer.initUiFrameDomain()
        DomainInitializer.initClientSocketDomain()
        DomainInitializer.initTransmitterDomain()
        DomainInitializer.initTaskWorkerDomain()





