from shapely import Polygon, Point

from opengl_my_card_main_frame.infra.my_card_repository import MyCardRepository


class PreparingOkButton:

    __my_card_repository = MyCardRepository()
    def __init__(self, my_card_main_frame):

        self.my_card_main_frame = my_card_main_frame

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
            y = self.my_card_main_frame.winfo_reqheight() - y

            ok_button = self.my_card_main_frame.my_card_main_scene.get_ok_button()
            if self.is_point_inside_object(ok_button, (x, y)):
                print(f"create_deck_button -> mouse_click_event() clicked create_deck_button")

                self.__my_card_repository.set_prepare_message_visible(False)

        except Exception as e:
            print(f"create deck register button Error : {e}")

    def check_collision(self, x, y, vertices):
        print(f"checking collision: x:{x}, y:{y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max