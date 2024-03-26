from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl


class CreateDeckRegisterScreen:
    def __init__(self, my_card_main_frame):
        self.my_card_main_frame = my_card_main_frame
        # self.music_player_repository = MusicPlayerRepositoryImpl.getInstance()

    def mouse_click_event(self, event):
        # self.music_player_repository.play_sound_effect_of_mouse_on_click('menu_button_click')
        try:
            x, y = event.x, event.y
            y = self.my_card_main_frame.winfo_reqheight() - y

            # deck_button_rectangle_vertices = [(0.85 * self.my_card_main_frame.width,
            #                                    0.85 * self.my_card_main_frame.height),
            #                                   (self.my_card_main_frame.width - 50,
            #                                    0.85 * self.my_card_main_frame.height),
            #                                   (self.my_card_main_frame.width - 50,
            #                                    self.my_card_main_frame.height - 100),
            #                                   (0.85 * self.my_card_main_frame.width,
            #                                    self.my_card_main_frame.height - 100)]

            left_x_point = self.my_card_main_frame.width * 0.81601
            right_x_point = self.my_card_main_frame.width * 0.97564
            top_y_point = self.my_card_main_frame.height * 0.78051
            bottom_y_point = self.my_card_main_frame.height * 0.86023

            deck_button_rectangle_vertices = [
                (left_x_point, top_y_point),
                (right_x_point, top_y_point),
                (right_x_point, bottom_y_point),
                (left_x_point, bottom_y_point)
            ]

            # rectangle_size = 130
            # start_point = (1569, 746)
            # end_point = (start_point[0] + rectangle_size * 2.3, start_point[1] + rectangle_size * 0.55)
            # deck_button_rectangle_vertices = [
            #     (start_point[0], start_point[1]),
            #     (end_point[0], start_point[1]),
            #     (end_point[0], end_point[1]),
            #     (start_point[0], end_point[1])
            # ]

            if self.check_collision(x, y, deck_button_rectangle_vertices):
                self.my_card_main_frame.show_my_deck_register_screen = True
                self.my_card_main_frame.redraw()
                print("투명 화면, 덱 생성 화면 그려졌니?")

        except Exception as e:
            print(f"create deck register screen Error : {e}")

    def check_collision(self, x, y, vertices):
        # print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max
