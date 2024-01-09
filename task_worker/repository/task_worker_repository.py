import abc


class TaskWorkerRepository(abc.ABC):
    @abc.abstractmethod
    def save_task_worker(self, name, will_be_execute_function):
        pass
