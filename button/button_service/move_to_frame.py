from tkinter_shape.button_maker import ButtonMaker
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl

class MoveToFrame:
    __instance = None

    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas
        self.ui_frame_service = UiFrameServiceImpl.getInstance()

    def moveToFrameButton(self, go_to_frame):
        button = ButtonMaker(self.master, self.canvas)
        button.create_button(button_name="되돌아 가기", bg="black", relx=0.88, rely=0.90,
                             width=25, height=2,
                             work=self.switchFrame(go_to_frame))

    def switchFrame(self, menu_name):
        self.ui_frame_service.switchFrameWithMenuName(menu_name)