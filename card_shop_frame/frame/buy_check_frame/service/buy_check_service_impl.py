import tkinter
from PIL import ImageTk, Image

from card_shop_frame.frame.buy_check_frame.entity.buy_check_frame import BuyCheckFrame
from card_shop_frame.frame.buy_check_frame.service.buy_check_service import BuyCheckService
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from card_shop_frame.frame.buy_check_frame.service.request.free_random_card_request import FreeRandomCardRequest
from card_shop_frame.frame.buy_check_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from opengl_buy_random_card_frame.service.buy_random_card_frame_service_impl import BuyRandomCardFrameServiceImpl


class BuyCheckServiceImpl(BuyCheckService):
    __instance = None
    def __new__(cls):
        from card_shop_frame.service.card_shop_service_impl import CardShopMenuFrameServiceImpl
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__buyCheckRepository = BuyCheckRepositoryImpl.getInstance()
            cls.__instance.__cardShopMenuFrameService = CardShopMenuFrameServiceImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            #cls.__instance.__buyRandomCardFrameService = BuyRandomCardFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.legend_stack_count = 10


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


    def createBuyCheckUiFrame(self, rootWindow, switchFrameWithMenuName):
        buyCheckFrame = self.__buyCheckRepository.createBuyCheckFrame(rootWindow)

        def restore_frame(buyCheckFrame):
            self.__cardShopMenuFrameService.RestoreCardShopUiButton()
            buyCheckFrame.destroy()

        def count_down_confirmed_upper_legend():
            self.legend_stack_count = self.legend_stack_count - 1




        def yes_click_button(buyCheckFrame):
            # title_bar_height = root.winfo_rooty()
            if self.legend_stack_count == 0:
                responseData = self.__buyCheckRepository.requestBuyRandomCard(
                    BuyRandomCardRequest(sessionInfo=self.__sessionRepository.get_session_info(), race_name=self.findRace(), is_confirmed_upper_legend=True))
                self.legend_stack_count = 10
            else:
                responseData = self.__buyCheckRepository.requestBuyRandomCard(
                    BuyRandomCardRequest(sessionInfo=self.__sessionRepository.get_session_info(),
                                         race_name=self.findRace(), is_confirmed_upper_legend=False))

            is_success = responseData.get('is_success')
            print(f"is_success: {is_success}")
            cardlist = responseData.get('card_id_list')
            print(f"cardlist: {cardlist}")
            if is_success == True:
                self.__buyCheckRepository.clearRandomCardList()
                self.__buyCheckRepository.clear_random_buy_card_object_list()
                self.__buyCheckRepository.setRandomCardList(cardlist)
                # self.__buyCheckRepository.create_random_buy_list()
                self.__buyCheckRepository.set_need_to_redraw(True)
                count_down_confirmed_upper_legend()
                self.__cardShopMenuFrameService.RestoreCardShopUiButton()
                switchFrameWithMenuName("buy-random-card")
                buyCheckFrame.destroy()
            else:
                not_have_money_label = tkinter.Label(buyCheckFrame, text="골드가 부족합니다.", font=("Helvetica", 10),
                                                     fg="red", bg="#F7F8E0", anchor="center", justify="center")
                not_have_money_label.place(relx=0.25, rely=0.8,  anchor="center", bordermode="outside")

        def resize_image(image_path, width, height):
            image_origin = Image.open(image_path)
            resized_image = image_origin.resize((width, height), Image.ANTIALIAS)
            return ImageTk.PhotoImage(resized_image)

        self.image_select_all = resize_image("local_storage/shop_image/select_all.png", 500, 700)
        self.image_select_undead = resize_image("local_storage/shop_image/select_undead.png", 500, 700)
        self.image_select_trent = resize_image("local_storage/shop_image/select_trent.png", 500, 700)
        self.image_select_human = resize_image("local_storage/shop_image/select_human.png", 500, 700)

        self.button_image_yes = resize_image("local_storage/shop_image/yes_button.png", 170, 50)
        self.button_image_no = resize_image("local_storage/shop_image/no_button.png", 170, 50)

        if self.__cardShopMenuFrameRepository.getRace() == "전체":
            self.screen_image = self.image_select_all
            self.image_width = self.image_select_all.width()
            self.image_height = self.image_select_all.height()

        elif self.__cardShopMenuFrameRepository.getRace() == "언데드":
            self.screen_image = self.image_select_undead
            self.image_width = self.image_select_undead.width()
            self.image_height = self.image_select_undead.height()

        elif self.__cardShopMenuFrameRepository.getRace() == "트랜트":
            self.screen_image = self.image_select_trent
            self.image_width = self.image_select_trent.width()
            self.image_height = self.image_select_trent.height()

        elif self.__cardShopMenuFrameRepository.getRace() == "휴먼":
            self.screen_image = self.image_select_human
            self.image_width = self.image_select_human.width()
            self.image_height = self.image_select_human.height()


        buyCheckFrame.set_image(self.screen_image)

        yes_button = tkinter.Button(buyCheckFrame,
                                    image=self.button_image_yes,
                                    bd=0, highlightthickness=0,
                                    command=lambda: yes_click_button(buyCheckFrame),
                                    width=170, height=50)

        yes_button.place(relx=0.29, rely=0.88, anchor="center")

        no_button = tkinter.Button(buyCheckFrame,
                                   image=self.button_image_no,
                                   bd=0, highlightthickness=0,
                                   command=lambda: restore_frame(buyCheckFrame),
                                   width=170, height=50)

        no_button.place(relx=0.71, rely=0.88, anchor="center")

        buyCheckFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        return buyCheckFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("BuyCheckServiceImpl: injectTransmitIpcChannel()")
        self.__buyCheckRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("BuyCheckServiceImpl: injectReceiveIpcChannel()")
        self.__buyCheckRepository.saveReceiveIpcChannel(receiveIpcChannel)
