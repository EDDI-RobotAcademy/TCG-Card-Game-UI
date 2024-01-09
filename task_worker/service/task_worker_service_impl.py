from task_worker.repository.task_worker_repository_impl import TaskWorkerRepositoryImpl
from task_worker.service.task_worker_service import TaskWorkerService


class TaskWorkerServiceImpl(TaskWorkerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__taskWorkerRepository = TaskWorkerRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createTaskWorker(self, name, will_be_execute_function):
        print("TaskWorkerServiceImpl: createTaskWorker()")

        self.__taskWorkerRepository.saveTaskWorker(name, will_be_execute_function)

    def executeTaskWorker(self, name):
        print("TaskWorkerServiceImpl: executeTaskWorker()")

        self.__taskWorkerRepository.executeTask(name)





