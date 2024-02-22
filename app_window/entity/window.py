import tkinter

from screeninfo import get_monitors


class Window(tkinter.Tk):
    def __init__(self, title, geometry, background_color, resizable):
        super().__init__()
        # self.title(title)
        # self.geometry(geometry)
        # self.configure(bg=background_color)
        # self.resizable(*resizable)

        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        self.title("Full Screen Window")
        self.geometry(f"{target_monitor.width}x{target_monitor.height}+{target_monitor.x}+{target_monitor.y}")
        self.configure(bg="white")
        self.resizable(True, True)

