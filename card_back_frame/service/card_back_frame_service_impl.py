
from card_back_frame.repository.card_back_frame_repository_impl import CardBackFrameRepositoryImpl
from card_back_frame.service.card_back_frame_service import CardBackFrameService
class CardBackFrameServiceImpl(CardBackFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardBackFrameRepository = CardBackFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardBackUiFrame(self, rootWindow):
        CardBackFrame = self.__cardBackFrameRepository.createCardBackFrame(rootWindow)

        return CardBackFrame