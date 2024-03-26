from colorama import Fore, Style
from shapely import Polygon, Point


class DrawAgainButton:

    # my_card_repository = MyCardRepository.getInstance()

    def __init__(self, master, buy_random_card_frame):
        self.master = master
        self.buy_random_card_frame = buy_random_card_frame
        # self.buy_random_card_scene = self.buy_random_card_frame.buy_random_card_scene

        self.width_ratio = 1
        self.height_ratio = 1

    def is_point_inside_object(self, object, coordinates):
        x, y = coordinates
        y *= -1

        object_vertices = object.get_vertices()

        ratio_applied_valid_object = [(x * self.width_ratio, y * self.height_ratio) for x, y in object_vertices]
        print(f"draw_again_button -> is_point_inside_object() - ratio_applied_valid_your_field: {ratio_applied_valid_object}")
        print(f"x: {x * self.width_ratio}, y: {y * self.height_ratio}")

        poly = Polygon(ratio_applied_valid_object)
        point = Point(x, y)

        return point.within(poly)

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.buy_random_card_frame.winfo_reqheight() - y

            draw_again_button = self.buy_random_card_frame.buy_random_card_scene.get_again_button()
            if self.is_point_inside_object(draw_again_button, (x, y)):
                print(f"draw_again_button -> mouse_click_event() clicked draw_again_button")

                # 여기서 화면 띄우기 뽑기 진행하시면 됩니다

        except Exception as e:
            print(f"next page button Error : {e}")