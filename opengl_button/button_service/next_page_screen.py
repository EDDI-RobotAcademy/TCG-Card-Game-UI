class NextPageScreen:
    def __init__(self, my_card_main_frame):

        self.my_card_main_frame = my_card_main_frame

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.my_card_main_frame.winfo_reqheight() - y


            deck_button_rectangle_vertices = [(0.85 * self.my_card_main_frame.width - self.my_card_main_frame.width * 0.25,
                                               0.85 * self.my_card_main_frame.height + 90),
                                              (self.my_card_main_frame.width - 50 - self.my_card_main_frame.width * 0.25,
                                               0.85 * self.my_card_main_frame.height + 90),
                                              (self.my_card_main_frame.width - 50 - self.my_card_main_frame.width * 0.25,
                                               self.my_card_main_frame.height - 100 + 90),
                                              (0.85 * self.my_card_main_frame.width - self.my_card_main_frame.width * 0.25,
                                               self.my_card_main_frame.height - 100 + 90)]

            if self.check_collision(x, y, deck_button_rectangle_vertices):

                # 화면에 있는 것들 싹 다 지워야 함.
                self.my_card_main_frame.clear_screen()
                print("다 지워졌니?")

                # 다시 내 카드 화면 그려...
                self.my_card_main_frame.second_page_card_draw()
                print("다 그려졌니....?")

        except Exception as e:
            print(f"create deck register Error : {e}")

    def check_collision(self, x, y, vertices):
        print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max