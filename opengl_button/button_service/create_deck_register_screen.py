from opengl_my_card_main_frame.renderer.my_deck_register_frame_renderer import MyDeckRegisterFrameRenderer


class CreateDeckRegisterScreen:
    __instance = None

    def __init__(self, master, frame):
        self.master = master
        self.my_card_main_frame = frame

    def buttonBind(self):
        print("바인드")
        self.my_card_main_frame.bind("<Button-1>", self.mouse_click_event)

    def mouse_click_event(self, event):

        try:
            x, y = event.x, event.y
            y = self.master.winfo_reqheight() - y

            button_rectangle_vertices = [(0.85 * self.my_card_main_frame.width, 0.85 * self.my_card_main_frame.height),
                                         (self.my_card_main_frame.width - 50, 0.85 * self.my_card_main_frame.height),
                                         (self.my_card_main_frame.width - 50, self.my_card_main_frame.height - 100),
                                         (0.85 * self.my_card_main_frame.width, self.my_card_main_frame.height - 100)]

            if self.check_collision(x, y, button_rectangle_vertices):
                self.my_card_main_frame.show_my_deck_register_screen = True
                self.my_card_main_frame.redraw()
                # print("내 카드 화면에서 Deck Register Scene 잘 가져 왔니?")
                # my_scene = self.my_card_main_frame.getMyDeckRegisterScene()
                # print("Deck Register Scene 그려야지~")
                # self.renderer = MyDeckRegisterFrameRenderer(my_scene, self.my_card_main_frame)
                # self.renderer.render()
                # print("Deck Register Scene 그려졌고~~")

        except Exception as e:
            print(f"create deck register Error : {e}")


    def check_collision(self, x, y, vertices):
        print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max