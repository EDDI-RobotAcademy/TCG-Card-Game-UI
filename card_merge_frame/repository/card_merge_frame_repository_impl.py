from card_merge_frame.entity.card_merge_frame import CardMergeFrame
from card_merge_frame.repository.card_merge_frame_repository import CardMergeFrameRepository


class CardMergeFrameRepositoryImpl(CardMergeFrameRepository):
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

    def createCardMergeFrame(self, rootWindow):
        print("CardFrameRepositoryImpl: createCardFrame()")
        cardMergeFrame = CardMergeFrame(rootWindow)

        return cardMergeFrame