from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene


class NextPageScreen:
    def __init__(self, my_card_main_frame, page_manager):

        self.my_card_main_frame = my_card_main_frame
        self.page_manager = page_manager

        self.my_card_main_scene = MyCardMainScene()

        self.width_ratio = 1
        self.height_ratio = 1

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.my_card_main_frame.winfo_reqheight() - y

            # deck_button_rectangle_vertices = [(0.85 * self.my_card_main_frame.width - self.my_card_main_frame.width * 0.25,
            #                                    0.85 * self.my_card_main_frame.height + 90),
            #                                   (self.my_card_main_frame.width - 50 - self.my_card_main_frame.width * 0.25,
            #                                    0.85 * self.my_card_main_frame.height + 90),
            #                                   (self.my_card_main_frame.width - 50 - self.my_card_main_frame.width * 0.25,
            #                                    self.my_card_main_frame.height - 100 + 90),
            #                                   (0.85 * self.my_card_main_frame.width - self.my_card_main_frame.width * 0.25,
            #                                    self.my_card_main_frame.height - 100 + 90)]
            #
            # if self.check_collision(x, y, deck_button_rectangle_vertices):
            #     print("첫 번째 페이지 입니다.")
            #     if event:
            #         self.page_manager.go_to_next_page()
            #         self.handle_page_transition()

            # next_left_x_point = self.my_card_main_frame.width * 0.730
            # next_right_x_point = self.my_card_main_frame.width * 0.786
            # next_top_y_point = self.my_card_main_frame.height * 0.483
            # next_bottom_y_point = self.my_card_main_frame.height * 0.553
            #
            # deck_button_rectangle_vertices = [
            #     (next_left_x_point, next_top_y_point),
            #     (next_right_x_point, next_top_y_point),
            #     (next_right_x_point, next_bottom_y_point),
            #     (next_left_x_point, next_bottom_y_point)
            # ]
            #
            # if self.check_collision(x, y, deck_button_rectangle_vertices):
            #     print("첫 번째 페이지 입니다.")
            #     if event:
            #         self.page_manager.go_to_next_page()
                    # self.handle_page_transition()


            # if self.is_point_inside_next_button((x, y)):
            #     print("첫 번째 페이지 입니다.")
            #     if event:
            #         self.page_manager.go_to_next_page()
            #         self.handle_page_transition()

        except Exception as e:
            print(f"next page button Error : {e}")

    def handle_page_transition(self):
        current_page = self.page_manager.get_current_page()

        if current_page == 2:
            print(f"현재 페이지는?{self.page_manager.get_current_page}")
            self.my_card_main_frame.clear_screen()
            print("기존의 내 카드 화면 다 삭제")
            self.my_card_main_frame.show_second_page_card_screen = True
            self.my_card_main_frame.second_page_card_draw()
            print("현재 2 페이지 입니다.")

        # 2 페이지 에서 버튼을 더 눌러도 current_page 숫자 안 올라감!
        elif current_page >= 3:
            self.page_manager.init_current_page_next_button()
            print("마지막 페이지 입니다. 더 이상 이동할 페이지가 없습니다.")

        # elif current_page == 3:
        #     self.my_card_main_frame.show_second_page_card_screen = False
        #     self.my_card_main_frame.clear_screen()
        #     self.my_card_main_frame.show_third_page_card_screen = True
        #     self.my_card_main_frame.third_page_card_draw()
        #     print("현재 3 페이지 입니다.")
        #
        # elif current_page == 4:
        #     self.my_card_main_frame.show_third_page_card_screen = False
        #     self.my_card_main_frame.clear_screen()
        #     self.my_card_main_frame.show_fourth_page_card_screen = True
        #     self.my_card_main_frame.fourth_page_card_draw()
        #     print("현재 4 페이지 입니다.")
        #
        # elif current_page == 5:
        #     self.my_card_main_frame.show_fourth_page_card_screen = False
        #     self.my_card_main_frame.clear_screen()
        #     self.my_card_main_frame.show_fifth_page_card_screen = True
        #     self.my_card_main_frame.fifth_page_card_draw()
        #     print("현재 5 페이지 입니다.")


    def check_collision(self, x, y, vertices):
        # print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max

    def is_point_inside_next_button(self, point):
        point_x, point_y = point
        point_y *= -1

        button_list = self.my_card_main_scene.get_button_list()
        next_gold_button_hand = button_list[2]
        print(f"next_gold_button 잘 가져와짐?: {next_gold_button_hand}")
        # print(f"point: {point}")

        translated_vertices = [
            (x * self.width_ratio + next_gold_button_hand.local_translation[0] * self.width_ratio,
             y * self.height_ratio + next_gold_button_hand.local_translation[1] * self.height_ratio)
            for x, y in next_gold_button_hand.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("next button clicked!")
        return True