from ui_frame.repository.ui_frame_repository import UiFrameRepository


class UiFrameRepositoryImpl(UiFrameRepository):
    __instance = None
    __currentFrame = None
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

    def setCurrentFrame(self, currentFrame):
        self.__currentFrame = currentFrame

    def getWindowFrameList(self):
        print("UiFrameRepositoryImpl: getWindowFrameList()")
        return self.__windowFrameList

    def registerUiFrame(self, name, newFrame):
        print("UiFrameRepositoryImpl: registerUiFrame()")
        self.__windowFrameList[name] = newFrame
        self.__currentFrame = newFrame

    def switchFrameWithMenuName(self, name: str):
        print("UiFrameRepositoryImpl: switchFrameWithMenuName()")

        foundUiFrame = self.__windowFrameList[name]

        if foundUiFrame is None:
            print("UiFrame 등록 및 전환에 문제가 발생했습니다")

        if self.__currentFrame is not None:
            print("기존 Frame 해제")
            self.__currentFrame.pack_forget()

        foundUiFrame.pack(expand=True, fill="both")
        self.__currentFrame = foundUiFrame

