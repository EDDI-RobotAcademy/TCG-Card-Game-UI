from my_card_frame.entity.my_card_frame import MyCardFrame
from my_card_frame.repository.my_card_frame_repository import MyCardFrameRepository


class MyCardFrameRepositoryImpl(MyCardFrameRepository):
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

    def createMyCardFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createMainMenuFrame()")
        myCardFrame = MyCardFrame(rootWindow, width=1200, height=800)

        return myCardFrame
