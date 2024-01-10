from app_window.service.window_service_impl import WindowServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl


class DomainInitializer:
    def __init__(self):
        self.initMainWindowDomain()
        self.initTaskWorkerDomain()

    @staticmethod
    def initMainWindowDomain():
        WindowServiceImpl.getInstance()

    @staticmethod
    def initTaskWorkerDomain():
        TaskWorkerServiceImpl.getInstance()

    @staticmethod
    def initEachDomain():
        DomainInitializer.initMainWindowDomain()
        DomainInitializer.initTaskWorkerDomain()


