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
        self.submit_button = button.create_button(button_name="확인", bg="black",
                                                    width=25, height=2)
    def buttonPlace(self, relx=0.5, rely=0.65):
        self.submit_button.place(relx=relx, rely=rely, anchor="center")

    def buttonBind(self):
        self.submit_button.bind("<Button-1>", lambda event: self.toggle_visibility())

    def toggle_visibility(self):
        print("이것은 확인 버튼을 클릭 했을 때 발생하는 이벤트!")
        # scene을 불러옴.
        my_deck_register_scene = self.my_card_main_frame.getScene()

        # 입력한 텍스트를 가져와서 등록
        for textbox_string in my_deck_register_scene.get_deck_name_list():
            text = textbox_string.get()
        entry_deck_name = text
        self.my_deck_register_frame_service.on_deck_register_click(entry_deck_name)

        # 확인 버튼을 누르면 덱 생성 화면 사라져야 함.
        self.my_card_main_frame.getCanvas().delete("all")

        #TODO: 텍스트 박스가 실행할 때마다 생겨서 전부 지워져야 하는데,,
        print(f"텍스트 박스 몇 개여 이게 : {my_deck_register_scene.get_text_box()}")
        for i in range(len(my_deck_register_scene.get_text_box())):
            my_deck_register_scene.get_text_box()[i].hideTextBox()
        self.submit_button.destroy()
        self.my_card_main_frame.redraw()


        #TODO: 아래는 덱 버튼 생성 코드. 미래 리펙토링 확정~
        try:
            deck_button= self.my_deck_register_frame_service.create_register_deck_button(self.my_card_main_frame.getCanvas(),
                                                                                         entry_deck_name)
            self.current_rely = 0.20
            my_deck_register_scene.add_deck_button_list(deck_button)
            print(f"생성한 버튼은?: {my_deck_register_scene.get_deck_button_list()}")
            for i in range(len(my_deck_register_scene.get_deck_button_list())):
                my_deck_register_scene.get_deck_button_list()[i].place(relx=0.88, rely=self.current_rely, anchor="center")
                self.current_rely += 0.1
                if len(my_deck_register_scene.get_deck_button_list()) > 6:
                    break
            #deck_button.bind("<Button-1>", self.make_my_deck_rectangle)
            #self.current_rely += 0.1
            print(f"버튼 위치 잘 변경 되었니?: {self.current_rely}")

        except Exception as e:
            print(f"An error occurred: {e}")



