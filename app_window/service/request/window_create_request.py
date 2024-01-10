from app_window.entity.window import Window


class WindowCreateRequest:
    def __init__(self, title="", geometry="800x600", background_color="#FFFFFF", resizable=(True, True)):
        self.__title = title
        self.__geometry = geometry
        self.__background_color = background_color
        self.__resizable = resizable

    def getTitle(self) -> str:
        return self.__title

    def getGeometry(self) -> str:
        return self.__geometry

    def getBackgroundColor(self) -> str:
        return self.__background_color

    def getResizable(self):
        return self.__resizable

    def toWindow(self):
        return Window(self.__title, self.__geometry, self.__background_color, self.__resizable)
