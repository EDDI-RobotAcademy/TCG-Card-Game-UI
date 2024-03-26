from shapely import Polygon, Point

from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl
from lobby_frame.service.request.check_game_money_request import CheckGameMoneyRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl


class BackToShopFrame:
    __receiveIpcChannel = None
    __transmitIpcChannel = None

    def __init__(self, master, target_frame):
        self.master = master
        self.target_frame = target_frame
        self.ui_frame_service = UiFrameServiceImpl.getInstance()
        self.session_repository = SessionRepositoryImpl.getInstance()
        self.card_shop_menu_frame_repository = CardShopMenuFrameRepositoryImpl.getInstance()

    def is_point_inside_object(self, object, coordinates):
        x, y = coordinates
        y *= -1

        object_vertices = object.get_vertices()

        ratio_applied_valid_object = [(x * self.target_frame.width, y * self.target_frame.height) for x, y in object_vertices]
        print(f"go_back_button -> is_point_inside_object() - ratio_applied_valid_your_field: {ratio_applied_valid_object}")
        print(f"x: {x * self.target_frame.width}, y: {y * self.target_frame.height}")

        poly = Polygon(ratio_applied_valid_object)
        point = Point(x, y)

        return point.within(poly)

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.master.winfo_reqheight() - y

            # rectangle_vertices = [(0.85 * self.target_frame.width, 0.85 * self.target_frame.height + 90),
            #                       (self.target_frame.width - 50, 0.85 * self.target_frame.height + 90),
            #                       (self.target_frame.width - 50, self.target_frame.height - 10),
            #                       (0.85 * self.target_frame.width, self.target_frame.height - 10)]
            rectangle_vertices = [(0.9016216 * self.target_frame.width, 0.1978346 * self.target_frame.height),
                        (0.97567567 * self.target_frame.width, 0.1978346 * self.target_frame.height),
                        (0.97567567 * self.target_frame.width, 0.258858 * self.target_frame.height),
                        (0.9016216 * self.target_frame.width, 0.258858 * self.target_frame.height)]

            # go_back_button = self.target_frame.buy_random_card_scene.get_go_to_back_button()
            # if self.is_point_inside_object(go_back_button, (x, y)):
            #     # TODO: ...... Need to Refactor
            #     from opengl_buy_random_card_frame.service.buy_random_card_frame_service_impl import BuyRandomCardFrameServiceImpl
            #     print(f"mouse_click_event() clicked go_back_button")
            #
            #     responseData = BuyRandomCardFrameServiceImpl.getInstance().requestCheckGameMoney(
            #         CheckGameMoneyRequest(self.session_repository.get_session_info()))
            #
            #     if responseData:
            #         self.card_shop_menu_frame_repository.setMyMoney(responseData.get("account_point"))
            #         from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import \
            #             MyGameMoneyFrameServiceImpl
            #         MyGameMoneyFrameServiceImpl.getInstance().findMyMoney()
            #         self.switchFrame("card-shop-menu")
            #
            #     self.switchFrame("lobby-menu")

            if self.check_collision(x, y, rectangle_vertices):
                from opengl_buy_random_card_frame.service.buy_random_card_frame_service_impl import \
                    BuyRandomCardFrameServiceImpl
                responseData = BuyRandomCardFrameServiceImpl.getInstance().requestCheckGameMoney(CheckGameMoneyRequest(self.session_repository.get_session_info()))

                if responseData:
                    self.card_shop_menu_frame_repository.setMyMoney(responseData.get("account_point"))
                    from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import \
                        MyGameMoneyFrameServiceImpl
                    MyGameMoneyFrameServiceImpl.getInstance().findMyMoney()
                    self.switchFrame("lobby-menu")

            # self.buy_random_card_scene.add_go_to_back_button(go_to_back_button)
            #
            # if self.check_collision(x, y, rectangle_vertices):
            #     from opengl_buy_random_card_frame.service.buy_random_card_frame_service_impl import \
            #         BuyRandomCardFrameServiceImpl
            #     responseData = BuyRandomCardFrameServiceImpl.getInstance().requestCheckGameMoney(CheckGameMoneyRequest(self.session_repository.get_session_info()))
            #
            #     if responseData:
            #         self.card_shop_menu_frame_repository.setMyMoney(responseData.get("account_point"))
            #         from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import \
            #             MyGameMoneyFrameServiceImpl
            #         MyGameMoneyFrameServiceImpl.getInstance().findMyMoney()
            #         self.switchFrame("card-shop-menu")

        except Exception as e:
            print(f"create deck register Error : {e}")

    def check_collision(self, x, y, vertices):
        # print(f"checking collision: x: {x}, y: {y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max

    def switchFrame(self, menu):
        self.ui_frame_service.switchFrameWithMenuName(menu)
