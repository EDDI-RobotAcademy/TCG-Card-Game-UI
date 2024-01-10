from app_window.repository.window_repository_impl import WindowRepositoryImpl
from app_window.service.request.window_create_request import WindowCreateRequest
from app_window.service.window_service import WindowService


class WindowServiceImpl(WindowService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__windowRepository = WindowRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createStartWindow(self):
        print("WindowServiceImpl: createStartWindow()")

        return self.__windowRepository.createNewWindow(WindowCreateRequest(
            title="EDDI TCG Card Battle",
            geometry="1200x800+50+50",
            background_color="#000000",
            resizable=(True, True)
        ))

