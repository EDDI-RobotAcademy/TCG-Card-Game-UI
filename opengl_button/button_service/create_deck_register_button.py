from opengl_my_deck_register_frame.service.my_deck_register_frame_service_impl import MyDeckRegisterFrameServiceImpl
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl


# class CreateDeckButton:
#     __instance = None
#
#     def __init__(self, master, frame):
#         self.master = master
#         self.my_card_main_frame = frame
#         self.my_deck_register_frame_service = MyDeckRegisterFrameServiceImpl.getInstance()
#
#     def createDeckButton(self):
#         button = ButtonMaker(self.master, self.my_card_main_frame.getCanvas())
#         self.submit_button = button.create_button(button_name="확인", bg="black",
#                                                     width=25, height=2)
#     def buttonPlace(self, relx=0.5, rely=0.65):
#         self.submit_button.place(relx=relx, rely=rely, anchor="center")
#
#     def buttonBind(self):
#         self.submit_button.bind("<Button-1>", lambda event: self.toggle_visibility())
#
#     def toggle_visibility(self):
#         print("이것은 확인 버튼을 클릭 했을 때 발생하는 이벤트!")
#         # scene을 불러옴.
#         my_deck_register_scene = self.my_card_main_frame.getScene()
#
#         # 입력한 텍스트를 가져와서 등록
#         for textbox_string in my_deck_register_scene.get_deck_name_list():
#             text = textbox_string.get()
#         entry_deck_name = text
#         self.my_deck_register_frame_service.on_deck_register_click(entry_deck_name)
#
#         # 확인 버튼을 누르면 덱 생성 화면 사라져야 함.
#         self.my_card_main_frame.getCanvas().delete("all")
#
#         #TODO: 텍스트 박스가 실행할 때마다 생겨서 전부 지워져야 하는데,,
#         print(f"텍스트 박스 몇 개여 이게 : {my_deck_register_scene.get_text_box()}")
#         for i in range(len(my_deck_register_scene.get_text_box())):
#             my_deck_register_scene.get_text_box()[i].hideTextBox()
#         self.submit_button.destroy()
#         self.my_card_main_frame.redraw()
#
#
#         #TODO: 아래는 덱 버튼 생성 코드. 미래 리펙토링 확정~
#         try:
#             deck_button= self.my_deck_register_frame_service.create_register_deck_button(self.my_card_main_frame.getCanvas(),
#                                                                                          entry_deck_name)
#             self.current_rely = 0.20
#             my_deck_register_scene.add_deck_button_list(deck_button)
#             print(f"생성한 버튼은?: {my_deck_register_scene.get_deck_button_list()}")
#             for i in range(len(my_deck_register_scene.get_deck_button_list())):
#                 my_deck_register_scene.get_deck_button_list()[i].place(relx=0.88, rely=self.current_rely, anchor="center")
#                 self.current_rely += 0.1
#                 if len(my_deck_register_scene.get_deck_button_list()) > 6:
#                     break
#             #deck_button.bind("<Button-1>", self.make_my_deck_rectangle)
#             #self.current_rely += 0.1
#             print(f"버튼 위치 잘 변경 되었니?: {self.current_rely}")
#
#         except Exception as e:
#             print(f"An error occurred: {e}")



class CreateDeckRegisterButton:
    def __init__(self, my_card_main_frame):

        self.my_card_main_frame = my_card_main_frame
        self.my_deck_register_frame_service = MyDeckRegisterFrameServiceImpl.getInstance()

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.my_card_main_frame.winfo_reqheight() - y

            center_x = 0.5 * self.my_card_main_frame.width
            center_y = 0.5 * self.my_card_main_frame.height
            button_width = 0.15 * self.my_card_main_frame.width
            button_height = 0.06 * self.my_card_main_frame.height
            ok_button_y_offset = 0.8 * 0.5 * self.my_card_main_frame.height
            ok_button_x_offset = 0.25 * 0.5 * self.my_card_main_frame.width

            deck_button_rectangle_vertices = [(center_x - 0.5 * button_width + ok_button_x_offset,
                                               center_y - 0.5 * 0.5 * self.my_card_main_frame.height - button_height + ok_button_y_offset),
                                              (center_x + 0.5 * button_width + ok_button_x_offset,
                                               center_y - 0.5 * 0.5 * self.my_card_main_frame.height - button_height + ok_button_y_offset),
                                              (center_x + 0.5 * button_width + ok_button_x_offset,
                                               center_y - 0.5 * 0.5 * self.my_card_main_frame.height + ok_button_y_offset),
                                              (center_x - 0.5 * button_width + ok_button_x_offset,
                                               center_y - 0.5 * 0.5 * self.my_card_main_frame.height + ok_button_y_offset)]

            if self.my_card_main_frame.show_my_deck_register_screen is True and self.check_collision(x, y, deck_button_rectangle_vertices):
                # 입력한 텍스트를 가져오기
                deck_name = self.my_card_main_frame.getString()
                self.my_card_main_frame.getMyDeckRegisterScene().add_deck_name_list(deck_name)
                print(f"생성할 덱 이름 잘 들어 왔냐?{self.my_card_main_frame.getMyDeckRegisterScene().get_deck_name_list()}")

                for text in self.my_card_main_frame.getMyDeckRegisterScene().get_deck_name_list():
                    print(f"text:{text}")
                    self.my_deck_register_frame_service.on_deck_register_click(text)
                if event: # 확인 버튼을 클릭했을 때
                    self.my_card_main_frame.show_my_deck_register_screen = False
                    # 화면에 있는 것들 싹 다 지워야 함.
                    self.my_card_main_frame.clear_screen()
                    # self.my_card_main_frame.getTextBox().destroy()
                    self.destroy_entry()

                    # 다시 내 카드 화면 그려...
                    self.my_card_main_frame.show_first_page_card_screen = True
                    self.my_card_main_frame.drawMyCardMainFrame()

                    print("다 지워졌니?")
                    # TODO: 준비중인 페이지 입니다 메세지 창 띄우기

        except Exception as e:
            print(f"create deck register button Error : {e}")

    def check_collision(self, x, y, vertices):
        print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max

    def destroy_entry(self):
        entry = self.my_card_main_frame.getTextBox()
        if entry:
            entry.destroy()
            self.entry = None
