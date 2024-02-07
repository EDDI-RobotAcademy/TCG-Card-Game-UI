from tkinter_shape.button_maker import ButtonMaker
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl

class MoveToFrame:
    __instance = None

    def __init__(self, master, frame):
        self.master = master
        self.my_card_main_frame = frame
        self.ui_frame_service = UiFrameServiceImpl.getInstance()

    def moveToFrameButton(self):
        button = ButtonMaker(self.master, self.my_card_main_frame.getCanvas())
        self.movebutton = button.create_button(button_name="되돌아 가기", bg="black",
                             width=25, height=2)

    def buttonPlace(self, relx=0.88, rely=0.90):
        self.movebutton.place(relx=relx, rely=rely, anchor="center")

    def buttonBind(self, menu):
        self.movebutton.bind("<Button-1>", lambda event: self.switchFrame(menu))

    def switchFrame(self, menu):
        self.ui_frame_service.switchFrameWithMenuName(menu)