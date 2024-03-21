from colorama import Fore, Style
from shapely import Polygon, Point

from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.infra.my_card_repository import MyCardRepository


class CreatePreviousPageScreen:

    my_card_repository = MyCardRepository.getInstance()

    def __init__(self, my_card_main_frame, page_manager):

        self.my_card_main_frame = my_card_main_frame
        self.page_manager = page_manager
        self.my_card_main_scene = my_card_main_frame.my_card_main_scene

        self.width_ratio = 1
        self.height_ratio = 1

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.my_card_main_frame.winfo_reqheight() - y

            prev_button = self.my_card_main_scene.get_prev_button()
            if self.is_point_inside_object(prev_button, (x, y)):
                print(f"prev_button_screen -> mouse_click_event() clicked next_button")
                print(f"{Fore.RED}current page number: {self.my_card_repository.get_current_my_card_page()}{Style.RESET_ALL}")

                self.my_card_repository.prev_my_card_page()

        except Exception as e:
            print(f"previous page button Error : {e}")

    def is_point_inside_object(self, object, coordinates):
        x, y = coordinates
        y *= -1

        object_vertices = object.get_vertices()

        ratio_applied_valid_object = [(x * self.width_ratio, y * self.height_ratio) for x, y in object_vertices]
        print(f"prev_page_screen -> is_point_inside_object() - ratio_applied_valid_your_field: {ratio_applied_valid_object}")
        print(f"x: {x * self.width_ratio}, y: {y * self.height_ratio}")

        poly = Polygon(ratio_applied_valid_object)
        point = Point(x, y)

        return point.within(poly)

    def handle_page_transition(self):
        current_page = self.page_manager.get_current_page()
        #print(f"이전 페이지 버튼 클릭! -> 첫 시작 페이지는?: {current_page}")

        # if current_page == 4:
        #     self.my_card_main_frame.show_fifth_page_card_screen = False
        #     self.my_card_main_frame.clear_screen()
        #     self.my_card_main_frame.show_fourth_page_card_screen = True
        #     self.my_card_main_frame.fourth_page_card_draw()
        #     print("현재 4 번째 페이지 입니다.")
        #
        # elif current_page == 3:
        #     self.my_card_main_frame.show_fourth_page_card_screen = False
        #     self.my_card_main_frame.clear_screen()
        #     self.my_card_main_frame.show_third_page_card_screen = True
        #     self.my_card_main_frame.third_page_card_draw()
        #     print("현재 3 번째 페이지 입니다.")

        if current_page == 2:
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

        # 첫 번째 페이지 에서 이전 버튼 눌렀을 때 current_page 횟수 줄어듬 방지.
        elif current_page < 1:
            self.page_manager.init_current_page_previous_button()
            print("현재 1 번째 페이지 입니다. 더 이상 이동할 페이지가 없습니다.")



    def check_collision(self, x, y, vertices):
        # print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max

    def is_point_inside_prev_button(self, point):
        point_x, point_y = point
        point_y *= -1
        # point_x = self.total_width - point_x

        prev_gold_button = self.my_card_main_scene.get_button_list()[3]
        # print(f"prev_gold_button: {prev_gold_button.get_vertices()}")
        # print(f"point -> x: {point_x}, y: {point_y}")

        translated_vertices = [
            (x * self.width_ratio + prev_gold_button.local_translation[0] * self.width_ratio,
             y * self.height_ratio + prev_gold_button.local_translation[1] * self.height_ratio)
            for x, y in prev_gold_button.get_vertices()
        ]

        if not (translated_vertices[0][0] <= point_x <= translated_vertices[2][0] and
                translated_vertices[0][1] <= point_y <= translated_vertices[2][1]):
            return False

        print("prev button clicked!")
        return True