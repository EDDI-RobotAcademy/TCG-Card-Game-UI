from opengl_my_card_main_frame.entity.my_deck_register_scene import MyDeckRegisterScene
from opengl_my_card_main_frame.frame.my_card_main_frame import MyCardMainFrame
from opengl_my_card_main_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer
from tkinter_shape.button_maker import ButtonMaker

class CreateDeckRegisterScreen:
    __instance = None

    def __init__(self, master, canvas, scene=None):
        self.master = master
        self.canvas = canvas
        self.scene = scene

        self.my_deck_register_scene = MyDeckRegisterScene()


        self.my_card_main_frame = MyCardMainFrame()

    def createDeckRegisterScreenButton(self):
        button = ButtonMaker(self.master, self.canvas)
        button.create_button(button_name="덱 생성", bg="black", relx=0.88, rely=0.80,
                             width=25, height=2,
                             work=self.toggle_visibility)

    def toggle_visibility(self):
        print("호출되냐아?")
        self.my_card_main_frame.make_my_deck_register_frame()
        print("지나가고~")
        self.renderer_after = MyDeckRegisterFrameRenderer(self.scene, self.my_card_main_frame)
        self.renderer_after.render()
        print("다되었고~~")
