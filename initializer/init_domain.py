from app_window.service.window_service_impl import WindowServiceImpl
from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from login_frame.service.login_menu_frame_service_impl import LoginMenuFrameServiceImpl
from main_frame.service.main_menu_frame_service_impl import MainMenuFrameServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
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
    def initClientSocketDomain():
        ClientSocketServiceImpl.getInstance()

    @staticmethod
    def initUiFrameDomain():
        UiFrameControllerImpl.getInstance()

    @staticmethod
    def initEachDomain():
        DomainInitializer.initRootWindowDomain()
        DomainInitializer.initMainMenuFrameDomain()
        DomainInitializer.initLoginMenuFrameDomain()
        DomainInitializer.initUiFrameDomain()
        DomainInitializer.initClientSocketDomain()
        DomainInitializer.initTaskWorkerDomain()



