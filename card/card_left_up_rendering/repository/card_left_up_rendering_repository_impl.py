import tkinter

from card.card_left_bottom_rendering.entity.card_left_bottom_rendering import CardLeftBottomRendering
from card.card_left_up_rendering.entity.card_left_up_rendering import CardLeftUpRendering
from card.card_left_up_rendering.repository.card_left_up_rendering_repository import CardLeftUpRenderingRepository


class CardLeftUpRenderingRepositoryImpl(CardLeftUpRenderingRepository):
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

    def createCardLeftUpRenderingFrame(self, rootWindow):
        print("CardFrameRepositoryImpl: createCardFrame()")
        cardLeftUpRendering = CardLeftUpRendering(rootWindow)
        circle_radius = 12  # 반지름 값, 적절하게 조절해주세요

        # Calculate the coordinates of the bounding box
        x1 = y1 = 25 - circle_radius
        x2 = y2 = 25 + circle_radius
        self.drawCircle(cardLeftUpRendering.canvas, x1, y1, x2, y2, fill='red', outline='black', width=1, text="Energy")

        return cardLeftUpRendering
    def drawCircle(self, canvas, x1, y1, x2, y2, text=None, **kwargs):

        # canvas.delete("all")
        # Calculate the center of the oval
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Calculate the radius
        radius_x = (x2 - x1) / 2
        radius_y = (y2 - y1) / 2

        # Increase the radius to make the circle twice as large
        radius_x *= 2
        radius_y *= 2

        # Adjust the coordinates of the oval
        x1 = center_x - radius_x
        y1 = center_y - radius_y
        x2 = center_x + radius_x
        y2 = center_y + radius_y

        # Draw the oval
        canvas.create_oval(x1, y1, x2, y2, **kwargs)

        if text:
            # Display text at the center
            canvas.create_text(center_x, center_y, text=text, fill='black')