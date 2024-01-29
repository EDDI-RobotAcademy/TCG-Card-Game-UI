from tests.my_deck_frame_legacy.entity.my_deck_frame import MyDeckFrame
from tests.my_deck_frame_legacy.repository.my_deck_frame_repository import MyDeckFrameRepository


class MyDeckFrameRepositoryImpl(MyDeckFrameRepository):
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

    def createMyDeckFrame(self, rootWindow):
        print("MyDeckFrameRepositoryImpl: createMyDeckFrame()")
        myDeckFrame = MyDeckFrame(rootWindow)

        return myDeckFrame