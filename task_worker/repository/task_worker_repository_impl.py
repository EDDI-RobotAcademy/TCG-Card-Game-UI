import multiprocessing

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

    def saveTaskWorker(self, name, will_be_execute_function):
        print("TaskWorkerRepositoryImpl: save_task_worker()")
        task_worker = TaskWorker(name, will_be_execute_function)
        self.__thread_worker_list[name] = task_worker

    def executeTask(self, name):
        print("TaskWorkerRepositoryImpl: execute_task()")
        found_named_task_worker = self.__thread_worker_list[name]
        execute_function = found_named_task_worker.getWillBeExecuteFunction()

        newTask = multiprocessing.Process(target=execute_function, args=(None,))
        print(f"newTask: {newTask}")
        found_named_task_worker.setTaskPid(newTask.pid)

        newTask.start()
        newTask.join()



