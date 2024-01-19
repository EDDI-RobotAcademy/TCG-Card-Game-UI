import tkinter

from card.card_left_bottom_rendering.repository.card_left_bottom_rendering_repository_impl import \
    CardLeftBottomRenderingRepositoryImpl
from card.card_left_bottom_rendering.service.card_left_bottom_rendering_service import CardLeftBottomRenderingService

class CardLeftBottomRenderingServiceImpl(CardLeftBottomRenderingService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardLeftBottomRenderingRepository = CardLeftBottomRenderingRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardBackUiFrame(self, rootWindow):
        cardLeftBottomRenderingRepository = self.__cardLeftBottomRenderingRepository.createCardLeftBottomRenderingFrame(rootWindow)
        # cardLeftBottomRenderingRepository.canvas = tkinter.Canvas(width=50, height=50)
        # cardLeftBottomRenderingRepository.canvas.pack()

        # radius = 50
        # center_x, center_y = 50, 50
        # cardLeftBottomRenderingRepository.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill='blue')

        return cardLeftBottomRenderingRepository