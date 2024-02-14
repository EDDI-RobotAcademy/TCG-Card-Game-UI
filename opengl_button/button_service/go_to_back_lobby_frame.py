from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl


class GoToBackLobbyFrame:
    def __init__(self, master, my_card_main_frame):
        self.master = master
        self.my_card_main_frame = my_card_main_frame
        self.ui_frame_service = UiFrameServiceImpl.getInstance()

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.master.winfo_reqheight() - y

            rectangle_vertices = [(0.85 * self.my_card_main_frame.width, 0.85 * self.my_card_main_frame.height + 90),
                                  (self.my_card_main_frame.width - 50, 0.85 * self.my_card_main_frame.height + 90),
                                  (self.my_card_main_frame.width - 50, self.my_card_main_frame.height - 10),
                                  (0.85 * self.my_card_main_frame.width, self.my_card_main_frame.height - 10)]

            if self.check_collision(x, y, rectangle_vertices):
                self.switchFrame("lobby-menu")

        except Exception as e:
            print(f"create deck register Error : {e}")

    def check_collision(self, x, y, vertices):
        print(f"checking collision: x: {x}, y: {y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max

    def switchFrame(self, menu):
        self.ui_frame_service.switchFrameWithMenuName(menu)
