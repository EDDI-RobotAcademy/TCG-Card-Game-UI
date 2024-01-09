import abc


class TaskWorkerService(abc.ABC):
    @abc.abstractmethod
    def createTaskWorker(self, name, will_be_execute_function):
        pass

    @abc.abstractmethod
    def executeTaskWorker(self, name):
        pass
