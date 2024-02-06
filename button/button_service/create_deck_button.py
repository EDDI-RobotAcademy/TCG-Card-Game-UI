from opengl_my_deck_register_frame.service.my_deck_register_frame_service_impl import MyDeckRegisterFrameServiceImpl
from tkinter_shape.button_maker import ButtonMaker

class CreateDeckButton:
    __instance = None

    def __init__(self, master, frame):
        self.master = master
        self.my_card_main_frame = frame
        self.my_deck_register_frame_service = MyDeckRegisterFrameServiceImpl.getInstance()

    def createDeckButton(self):
        button = ButtonMaker(self.master, self.my_card_main_frame.getCanvas())
        self.submit_button = button.create_button(button_name="확인", bg="black",relx=0.5, rely=0.65,
                                                    width=25, height=2,
                                                    work=self.toggle_visibility)

    def toggle_visibility(self):
        print("이것은 확인 버튼을 클릭 했을 때 발생하는 이벤트!")
        # scene을 불러옴.
        my_scene = self.my_card_main_frame.getScene()

        # 입력한 텍스트를 가져와서 등록
        for textbox_string in my_scene.get_deck_name_list():
            text = textbox_string.get()
        entry_deck_name = text
        self.my_deck_register_frame_service.on_deck_register_click(entry_deck_name)

        # 확인 버튼을 누르면 덱 생성 화면 사라져야 함.
        self.my_card_main_frame.getCanvas().delete("all")
        self.submit_button.destroy()
        my_scene.get_text_box()[0].hideTextBox()
        self.my_card_main_frame.redraw()

        #TODO: 덱 버튼 생성 코드 삽입 예정.