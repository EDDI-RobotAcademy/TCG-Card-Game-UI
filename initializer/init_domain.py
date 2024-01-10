from app_window.service.window_service_impl import WindowServiceImpl
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
    def initUiFrameDomain():
        UiFrameControllerImpl.getInstance()

    @staticmethod
    def initEachDomain():
        DomainInitializer.initRootWindowDomain()
        DomainInitializer.initUiFrameDomain()
        DomainInitializer.initTaskWorkerDomain()



