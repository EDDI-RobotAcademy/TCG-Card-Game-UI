class CreatePreviousPageScreen:
    def __init__(self, my_card_main_frame, page_manager):

        self.my_card_main_frame = my_card_main_frame
        self.page_manager = page_manager

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.my_card_main_frame.winfo_reqheight() - y


            before_page_button_rectangle_vertices = [(50, 0.85 * self.my_card_main_frame.height + 90),
                                                     (0.15 * self.my_card_main_frame.width, 0.85 * self.my_card_main_frame.height + 90),
                                                     (0.15 * self.my_card_main_frame.width, self.my_card_main_frame.height - 100 + 90),
                                                     (50, self.my_card_main_frame.height - 100 + 90)]

            if self.check_collision(x, y, before_page_button_rectangle_vertices):
                if event:
                    self.page_manager.go_to_previous_page()
                    self.handle_page_transition()


        except Exception as e:
            print(f"create deck register Error : {e}")

    def handle_page_transition(self):
        current_page = self.page_manager.get_current_page()
        print(f"이전 페이지 버튼 클릭! -> 첫 시작 페이지는?: {current_page}")

        if current_page == 4:
            self.my_card_main_frame.show_fifth_page_card_screen = False
            self.my_card_main_frame.clear_screen()
            self.my_card_main_frame.show_fourth_page_card_screen = True
            self.my_card_main_frame.fourth_page_card_draw()
            print("현재 4 번째 페이지 입니다.")

        elif current_page == 3:
            self.my_card_main_frame.show_fourth_page_card_screen = False
            self.my_card_main_frame.clear_screen()
            self.my_card_main_frame.show_third_page_card_screen = True
            self.my_card_main_frame.third_page_card_draw()
            print("현재 3 번째 페이지 입니다.")

        elif current_page == 2:
            self.my_card_main_frame.show_third_page_card_screen = False
            self.my_card_main_frame.clear_screen()
            self.my_card_main_frame.show_second_page_card_screen = True
            self.my_card_main_frame.second_page_card_draw()
            print("현재 2 번째 페이지 입니다.")

        elif current_page == 1:
            self.my_card_main_frame.show_second_page_card_screen = False
            self.my_card_main_frame.clear_screen()
            self.my_card_main_frame.show_first_page_card_screen = True
            self.my_card_main_frame.drawMyCardMainFrame()
            print("현재 1 번째 페이지 입니다.")


    def check_collision(self, x, y, vertices):
        # print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max