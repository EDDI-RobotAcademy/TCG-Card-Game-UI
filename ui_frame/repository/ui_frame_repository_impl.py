from ui_frame.repository.ui_frame_repository import UiFrameRepository


class UiFrameRepositoryImpl(UiFrameRepository):
    __instance = None
    __windowFrameList = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def getWindowFrameList(self):
        print("UiFrameRepositoryImpl: getWindowFrameList()")
        return self.__windowFrameList

    def registerUiFrame(self, name, newFrame):
        print("UiFrameRepositoryImpl: registerUiFrame()")
        self.__windowFrameList[name] = newFrame




