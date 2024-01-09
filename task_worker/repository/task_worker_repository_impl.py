from task_worker.entity.task_worker import TaskWorker
from task_worker.repository.task_worker_repository import TaskWorkerRepository


class TaskWorkerRepositoryImpl(TaskWorkerRepository):
    __instance = None
    __thread_worker_list = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_task_worker(self, name, will_be_execute_function):
        task_worker = TaskWorker(name, will_be_execute_function)
        self.__thread_worker_list[name] = task_worker


