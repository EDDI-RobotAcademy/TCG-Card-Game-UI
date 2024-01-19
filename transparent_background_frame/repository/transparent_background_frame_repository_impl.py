from PIL import Image, ImageTk

from transparent_background_frame.entity.transparent_background_frame import TransparentBackgroundFrame
from transparent_background_frame.repository.transparent_background_frame_repository import TransparentBackgroundFrameRepository


class TransparentBackgroundFrameRepositoryImpl(TransparentBackgroundFrameRepository):
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

    def __init__(self):
        self.photo_image = None

    def Create_rectangle(self, frame, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = frame.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.photo_image = ImageTk.PhotoImage(image)
            frame.canvas.create_image(x1, y1, image=self.photo_image, anchor='nw')

    def createTransparentBackgroundFrame(self, rootWindow):
        print("TransparentBackgroundFrameRepositoryImpl: createATransparentBackgroundFrame()")
        transparentBackgroundFrame = TransparentBackgroundFrame(rootWindow)
        self.Create_rectangle(transparentBackgroundFrame, 50, 50, 1250, 850, fill="black", alpha=0.5)

        return transparentBackgroundFrame