class Window:
    def __init__(self, title="", geometry="800x600", background_color="#FFFFFF", resizable=(True, True)):
        self.__title = title
        self.__geometry = geometry
        self.__background_color = background_color
        self.__resizable = resizable

    def get_title(self):
        return self.__title

    def get_geometry(self):
        return self.__geometry

    def get_background_color(self):
        return self.__background_color

    def get_resizable(self):
        return self.__resizable

