from card.card_left_bottom_rendering.service.card_left_bottom_rendering_service_impl import \
    CardLeftBottomRenderingServiceImpl
from card.card_left_up_rendering.service.card_left_up_rendering_service_impl import CardLeftUpRenderingServiceImpl
from card.card_right_bottom_rendering.service.card_right_bottom_rendering_service_impl import \
    CardRightBottomRenderingServiceImpl
from card.card_right_up_rendering.service.card_right_up_rendering_service_impl import CardRightUpRenderingServiceImpl
from card_back_frame.repository.card_back_frame_repository_impl import CardBackFrameRepositoryImpl
from card_back_frame.service.card_back_frame_service import CardBackFrameService
class CardBackFrameServiceImpl(CardBackFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardBackFrameRepository = CardBackFrameRepositoryImpl.getInstance()
            cls.__instance.__cardLeftBottomRenderingService = CardLeftBottomRenderingServiceImpl.getInstance()
            cls.__instance.__cardLeftUpRenderingService = CardLeftUpRenderingServiceImpl.getInstance()
            cls.__instance.__cardRightBottomRenderingService = CardRightBottomRenderingServiceImpl.getInstance()
            cls.__instance.__cardRightUpRenderingService = CardRightUpRenderingServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardBackUiFrame(self, rootWindow):
        CardBackFrame = self.__cardBackFrameRepository.createCardBackFrame(rootWindow)
        CardLeftBottom = self.__cardLeftBottomRenderingService.createCardLeftBottomRenderingUiFrame(CardBackFrame)
        CardLeftBottom.place(relx=0, rely=0.76)

        CardLeftUp = self.__cardLeftUpRenderingService.createCardLeftUpRenderingUiFrame(CardBackFrame)
        CardLeftUp.place(relx=0, rely=0)

        CardRightBottom = self.__cardRightBottomRenderingService.createCardRightBottomRenderingUiFrame(CardBackFrame)
        CardRightBottom.place(relx=0.60, rely=0)

        CardRightUp = self.__cardRightUpRenderingService.createCardRightUpRenderingUiFrame(CardBackFrame)
        CardRightUp.place(relx=0.6, rely=0.76)
        return CardBackFrame