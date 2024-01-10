from app_window.repository.window_repository import WindowRepository


class WindowRepositoryImpl(WindowRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createNewWindow(self, appWindowRequest):
        print("WindowRepositoryImpl: createNewWindow()")

        return appWindowRequest.toWindow()

