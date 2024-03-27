from shapely import Polygon, Point

from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from card_shop_frame.frame.buy_check_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
# from card_shop_frame.service.card_shop_service_impl import CardShopMenuFrameServiceImpl

from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage

class AgainYesButton:

    # my_card_repository = MyCardRepository.getInstance()
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __buy_check_repository = BuyCheckRepositoryImpl.getInstance()
    __cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
    __buyCheckRepository = BuyCheckRepositoryImpl.getInstance()
    __sessionRepository = SessionRepositoryImpl.getInstance()
    # __cardShopMenuFrameService = CardShopMenuFrameServiceImpl.getInstance()

    def __init__(self, master, buy_random_card_frame):
        self.master = master
        self.buy_random_card_frame = buy_random_card_frame

        self.width_ratio = 1
        self.height_ratio = 1

        self.legend_stack_count = 10

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

            draw_yes_button = self.buy_random_card_frame.buy_random_card_scene.get_yes_button()
            if self.is_point_inside_object(draw_yes_button, (x, y)):
                print(f"draw_again_button -> mouse_click_event() clicked draw_yes_button")
                pass

                # if self.legend_stack_count == 0:
                #     responseData = self.__buyCheckRepository.requestBuyRandomCard(
                #         BuyRandomCardRequest(sessionInfo=self.__sessionRepository.get_session_info(),
                #                              race_name=self.findRace(), is_confirmed_upper_legend=True))
                #     self.legend_stack_count = 10
                # else:
                #     responseData = self.__buyCheckRepository.requestBuyRandomCard(
                #         BuyRandomCardRequest(sessionInfo=self.__sessionRepository.get_session_info(),
                #                              race_name=self.findRace(), is_confirmed_upper_legend=False))
                #
                # is_success = responseData.get('is_success')
                # print(f"is_success: {is_success}")
                # cardlist = responseData.get('card_id_list')
                # print(f"cardlist: {cardlist}")
                # if is_success == True:
                #     self.__buyCheckRepository.clearRandomCardList()
                #     self.__buyCheckRepository.clear_random_buy_card_object_list()
                #     self.__buyCheckRepository.setRandomCardList(cardlist)
                #     # self.__buyCheckRepository.create_random_buy_list()
                #     self.__buyCheckRepository.set_need_to_redraw(True)
                #     self.count_down_confirmed_upper_legend()
                #     self.__cardShopMenuFrameService.RestoreCardShopUiButton()
                #     switchFrameWithMenuName("buy-random-card")
                #     buyCheckFrame.destroy()
                #
                # else:
                #
                #     pass



        except Exception as e:
            print(f"next page button Error : {e}")


    def count_down_confirmed_upper_legend(self):
        self.legend_stack_count = self.legend_stack_count - 1

    def findRace(self):
        race_mapping = {
            "전체": "Chaos",
            "언데드": "Undead",
            "트랜트": "Trent",
            "휴먼": "Human"
        }
        Race = self.__cardShopMenuFrameRepository.getRace()
        Eg_Race = race_mapping.get(Race, "Unknown")
        print(f"Eg_Race: {Eg_Race}")
        return Eg_Race