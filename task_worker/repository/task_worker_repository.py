import abc


class TaskWorkerRepository(abc.ABC):
    @abc.abstractmethod
    def saveTaskWorker(self, name, will_be_execute_function):
        pass

    @abc.abstractmethod
    def executeTask(self, name):
        pass
