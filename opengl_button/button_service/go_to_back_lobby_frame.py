from colorama import Fore, Style
from shapely import Polygon, Point

from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl


class GoToBackLobbyFrame:
    def __init__(self, master, my_card_main_frame):
        self.master = master
        self.my_card_main_frame = my_card_main_frame
        self.ui_frame_service = UiFrameServiceImpl.getInstance()
        self.music_player_repository = MusicPlayerRepositoryImpl.getInstance()

        self.my_card_main_scene = my_card_main_frame.my_card_main_scene

        self.width_ratio = 1
        self.height_ratio = 1

    def is_point_inside_object(self, object, coordinates):
        x, y = coordinates
        y *= -1

        object_vertices = object.get_vertices()

        ratio_applied_valid_object = [(x * self.width_ratio, y * self.height_ratio) for x, y in object_vertices]
        print(f"go_back_button -> is_point_inside_object() - ratio_applied_valid_your_field: {ratio_applied_valid_object}")
        print(f"x: {x * self.width_ratio}, y: {y * self.height_ratio}")

        poly = Polygon(ratio_applied_valid_object)
        point = Point(x, y)

        return point.within(poly)

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.master.winfo_reqheight() - y

            go_back_button = self.my_card_main_scene.get_go_back_button()
            if self.is_point_inside_object(go_back_button, (x, y)):
                self.music_player_repository.play_sound_effect_of_mouse_on_click('menu_button_click')
                print(f"mouse_click_event() clicked go_back_button")

                self.switchFrame("lobby-menu")

        except Exception as e:
            print(f"go back to lobby button Error : {e}")

    def check_collision(self, x, y, vertices):
        # print(f"checking collision: x: {x}, y: {y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max

    def switchFrame(self, menu):
        self.ui_frame_service.switchFrameWithMenuName(menu)
