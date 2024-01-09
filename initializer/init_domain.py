from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from window.service.window_service_impl import WindowServiceImpl


class DomainInitializer:
    def __init__(self):
        self.initMainWindowDomain()
        self.initTaskWorkerDomain()

    def initMainWindowDomain(self):
        WindowServiceImpl.getInstance()

    def initTaskWorkerDomain(self):
        TaskWorkerServiceImpl.getInstance()


