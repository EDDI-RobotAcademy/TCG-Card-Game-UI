from button.button_service.create_deck_button import CreateDeckButton
from opengl_my_card_main_frame_legacy_not_yet_deleted.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from tkinter_shape.button_maker import ButtonMaker

class CreateDeckRegisterScreen:
    __instance = None

    def __init__(self, master, frame):
        self.master = master
        self.my_card_main_frame = frame

    def createDeckRegisterScreenButton(self):
        button = ButtonMaker(self.master, self.my_card_main_frame.getCanvas())
        self.deck_button = button.create_button(button_name="덱 생성", bg="black",
                             width=25, height=2)
    def buttonPlace(self, relx=0.88, rely=0.80):
        self.deck_button.place(relx=relx, rely=rely, anchor="center")

    def buttonBind(self):
        self.deck_button.bind("<Button-1>", lambda event: self.toggle_visibility())

    def toggle_visibility(self):
        print("나의 카드 화면에서 scene 잘 가져왔니?")
        my_scene = self.my_card_main_frame.make_my_deck_register_frame()
        print("scene 그려야지~")
        self.renderer_after = MyDeckRegisterFrameRenderer(my_scene, self.my_card_main_frame)
        self.renderer_after.render()
        print("scene 그려졌고~~")

        button = CreateDeckButton(self.master, self.my_card_main_frame)
        button.createDeckButton()
        button.buttonPlace()
        button.buttonBind()


