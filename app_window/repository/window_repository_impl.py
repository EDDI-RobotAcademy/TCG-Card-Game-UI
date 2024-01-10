from app_window.repository.window_repository import WindowRepository


class WindowRepositoryImpl(WindowRepository):
    __instance = None
    __windowFrameList = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        print("WindowRepositoryImpl 초기화")

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createNewWindow(self, appWindowRequest):
        print("WindowRepositoryImpl: createNewWindow()")

        return appWindowRequest.toWindow()

    def getWindowFrameList(self):
        return self.__windowFrameList

