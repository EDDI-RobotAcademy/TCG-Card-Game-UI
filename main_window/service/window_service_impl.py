from main_window.service.request.window_create_request import WindowCreateRequest
from main_window.service.window_service import WindowService


class WindowServiceImpl(WindowService):
    __instance = None

    def __new__(cls, windowRepository):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__windowRepository = windowRepository
        return cls.__instance

    @classmethod
    def getInstance(cls, repository=None):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createStartWindow(self, menuName):
        print("WindowServiceImpl: createStartWindow()")

        self.__windowRepository.createNewWindow(menuName, WindowCreateRequest(
            "EDDI TCG Card Battle",
            "1200x800",
            "#000000",
            (True, True)
        ))

