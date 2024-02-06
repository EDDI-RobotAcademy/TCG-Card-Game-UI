from button.button_service.create_deck_button import CreateDeckButton
from opengl_my_card_main_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from tkinter_shape.button_maker import ButtonMaker

class CreateDeckRegisterScreen:
    __instance = None

    def __init__(self, master, frame):
        self.master = master
        self.my_card_main_frame = frame

    def createDeckRegisterScreenButton(self):
        button = ButtonMaker(self.master, self.my_card_main_frame.getCanvas())
        button.create_button(button_name="덱 생성", bg="black", relx=0.88, rely=0.80,
                             width=25, height=2,
                             work=self.toggle_visibility)

    def toggle_visibility(self):
        print("나의 카드 화면에서 scene 잘 가져왔니?")
        my_scene = self.my_card_main_frame.make_my_deck_register_frame()
        print("scene 그려야지~")
        self.renderer_after = MyDeckRegisterFrameRenderer(my_scene, self.my_card_main_frame)
        self.renderer_after.render()
        print("scene 그려졌고~~")


