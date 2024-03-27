from shapely import Polygon, Point

from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage

class AgainNoButton:

    # my_card_repository = MyCardRepository.getInstance()
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __buy_check_repository = BuyCheckRepositoryImpl.getInstance()

    def __init__(self, master, buy_random_card_frame):
        self.master = master
        self.buy_random_card_frame = buy_random_card_frame
        # self.buy_random_card_scene = self.buy_random_card_frame.buy_random_card_scene

        self.width_ratio = 1
        self.height_ratio = 1

        self.try_again_screen_visible = False

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

            draw_no_button = self.buy_random_card_frame.buy_random_card_scene.get_no_button()
            if self.is_point_inside_object(draw_no_button, (x, y)):
                print(f"draw_again_button -> mouse_click_event() clicked draw_again_button")

                self.__buy_check_repository.set_try_again_screen_visible(False)



        except Exception as e:
            print(f"next page button Error : {e}")