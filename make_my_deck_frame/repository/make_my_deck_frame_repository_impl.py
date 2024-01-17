from make_my_deck_frame.entity.make_my_deck_frame import MakeMyDeckFrame
from make_my_deck_frame.repository.make_my_deck_frame_repository import MakeMyDeckFrameRepository


class MakeMyDeckFrameRepositoryImpl(MakeMyDeckFrameRepository):
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

    def createMakeMyDeckFrame(self, rootWindow):
        print("MakeMyDeckFrameRepositoryImpl: createMakeMyDeckFrame()")
        makeMyDeckFrame = MakeMyDeckFrame(rootWindow)

        return makeMyDeckFrame