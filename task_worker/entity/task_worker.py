class TaskWorker:
    def __init__(self, name, will_be_execute_function):
        self.__taskPid = None
        self.__name = name
        self.__will_be_execute_function = will_be_execute_function

    def setTaskPid(self, taskPid: int):
        self.__taskPid = taskPid

    def getTaskPid(self) -> int:
        return self.__taskPid

    def getName(self):
        return self.__name

    def getWillBeExecuteFunction(self):
        return self.__will_be_execute_function

