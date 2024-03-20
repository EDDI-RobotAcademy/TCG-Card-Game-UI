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

    def mouse_click_event(self, event):
        try:
            x, y = event.x, event.y
            y = self.master.winfo_reqheight() - y

            rectangle_vertices = [(0.85 * self.target_frame.width, 0.85 * self.target_frame.height + 90),
                                  (self.target_frame.width - 50, 0.85 * self.target_frame.height + 90),
                                  (self.target_frame.width - 50, self.target_frame.height - 10),
                                  (0.85 * self.target_frame.width, self.target_frame.height - 10)]

            if self.check_collision(x, y, rectangle_vertices):
                from opengl_buy_random_card_frame.service.buy_random_card_frame_service_impl import \
                    BuyRandomCardFrameServiceImpl
                responseData = BuyRandomCardFrameServiceImpl.getInstance().requestCheckGameMoney(CheckGameMoneyRequest(self.session_repository.get_session_info()))

                if responseData:
                    self.card_shop_menu_frame_repository.setMyMoney(responseData.get("account_point"))
                    from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import \
                        MyGameMoneyFrameServiceImpl
                    MyGameMoneyFrameServiceImpl.getInstance().findMyMoney()
                    self.switchFrame("card-shop-menu")

        except Exception as e:
            print(f"create deck register Error : {e}")

    def check_collision(self, x, y, vertices):
        # print(f"checking collision: x: {x}, y: {y}")
        x_min, y_min = min(v[0] for v in vertices), min(v[1] for v in vertices)
        x_max, y_max = max(v[0] for v in vertices), max(v[1] for v in vertices)
        return x_min <= x <= x_max and y_min <= -y <= y_max

    def switchFrame(self, menu):
        self.ui_frame_service.switchFrameWithMenuName(menu)
