import tkinter
from PIL import ImageTk, Image

from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from card_shop_frame.service.card_shop_service import CardShopMenuFrameService
from card_shop_frame.frame.buy_check_frame.service.buy_check_service_impl import BuyCheckServiceImpl
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl
from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import MyGameMoneyFrameServiceImpl
from card_shop_frame.frame.shop_title_frame.service.shop_title_frame_service_impl import ShopTitleFrameServiceImpl
from card_shop_frame.frame.shop_button_frame.service.shop_button_frame_service_impl import ShopButtonFrameServiceImpl
from card_shop_frame.frame.select_race_ui_frame.service.select_race_ui_frame_service_impl import SelectRaceUiFrameServiceImpl
from lobby_frame.repository.lobby_menu_frame_repository_impl import LobbyMenuFrameRepositoryImpl
from session.repository.session_repository_impl import SessionRepositoryImpl
from lobby_frame.service.request.card_list_request import CardListRequest
from opengl_my_card_main_frame.infra.my_card_repository import MyCardRepository
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl


class CardShopMenuFrameServiceImpl(CardShopMenuFrameService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__buyCheckService = BuyCheckServiceImpl.getInstance()
            cls.__instance.__buyCheckRepository = BuyCheckRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__lobbyMenuFrameRepository = LobbyMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__myGameMoneyFrameService = MyGameMoneyFrameServiceImpl.getInstance()
            cls.__instance.__shopTitleFrameService = ShopTitleFrameServiceImpl.getInstance()
            cls.__instance.__shopButtonFrameService = ShopButtonFrameServiceImpl.getInstance()
            cls.__instance.__selectRaceFrameService = SelectRaceUiFrameServiceImpl.getInstance()
            cls.__instance.__myCardRepository = MyCardRepository.getInstance()
            cls.__instance.__musicPlayerRepository = MusicPlayerRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def DisabledCardShopUiButton(self):
        self.get_new_all_cards_button["state"] = "disabled"
        self.get_new_undead_cards_button["state"] = "disabled"
        self.get_new_trant_cards_button["state"] = "disabled"
        self.get_new_human_cards_button["state"] = "disabled"
        self.go_back_to_lobby_button["state"] = "disabled"
        self.my_card_button["state"] = "disabled"

    def RestoreCardShopUiButton(self):
        self.get_new_all_cards_button["state"] = "normal"
        self.get_new_undead_cards_button["state"] = "normal"
        self.get_new_trant_cards_button["state"] = "normal"
        self.get_new_human_cards_button["state"] = "normal"
        self.go_back_to_lobby_button["state"] = "normal"
        self.my_card_button["state"] = "normal"



    def createCardShopUiFrame(self, rootWindow, switchFrameWithMenuName):
        cardShopMenuFrame = self.__cardShopMenuFrameRepository.createCardShopMenuFrame(rootWindow)

        def buy_check_button_click(race):
            self.__cardShopMenuFrameRepository.setRace(race)
            self.__buyCheckService.createBuyCheckUiFrame(cardShopMenuFrame, switchFrameWithMenuName)
            self.DisabledCardShopUiButton()

        def onClickMyCard():
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')
            try:
                session_info = self.__sessionRepository.get_session_info()
                if session_info is not None:
                    responseData = self.__lobbyMenuFrameRepository.requestAccountCardList(
                        CardListRequest(session_info))

                    print(f"responseData: {responseData}")

                    if responseData is not None:
                        server_data = responseData.get("card_id_list")

                        self.__myCardRepository.save_my_card_to_dictionary_state(server_data)
                        print(f"my_card_dictionary: {self.__myCardRepository.get_my_card_dictionary_from_state()}")


                        # for i, number in enumerate(server_data):
                        #     for key, value in server_data[i].items():
                        #         self.card_data_list.append(int(key))
                        #         self.number_of_cards_list.append(int(value))
                        #         print(f"서버로 부터 카드 정보 잘 받았니?:{self.card_data_list}")
                        #         print(f"서버로 부터 카드 갯수 잘 받았니?: {self.number_of_cards_list}")

                        switchFrameWithMenuName("my-card-main")

                    else:
                        print("Invalid or missing response data.")

            except Exception as e:
                print(f"An error occurred: {e}")

        # shopTitleFrame = self.__shopTitleFrameService.createShopTitleUiFrame(cardShopMenuFrame, switchFrameWithMenuName)
        # shopTitleFrame.pack(side=tkinter.TOP)
        #
        # shopButtonFrame = self.__shopButtonFrameService.createShopButtonUiFrame(cardShopMenuFrame, switchFrameWithMenuName)
        # shopButtonFrame.pack(side=tkinter.LEFT, anchor=tkinter.S)
        #
        # selectRaceUiFrame = self.__selectRaceFrameService.createSelectRaceUiFrame(cardShopMenuFrame, switchFrameWithMenuName)
        # selectRaceUiFrame.pack(side=tkinter.RIGHT, anchor=tkinter.S)

        my_money_frame = self.__myGameMoneyFrameService.createMyGameMoneyUiFrame(cardShopMenuFrame)
        my_money_frame.place(relx=0.91, rely=0.06, relwidth=0.09, relheight=0.02, anchor="center")

        # 버튼 이미지를 resize
        self.button_image_select_all_origin = Image.open("local_storage/shop_image/all_button.png")
        select_all_button = self.button_image_select_all_origin.resize((295, 300))
        self.button_image_select_all = ImageTk.PhotoImage(select_all_button)

        self.button_image_select_undead_origin = Image.open("local_storage/shop_image/undead_button.png")
        select_undead_button = self.button_image_select_undead_origin.resize((295, 300))
        self.button_image_select_undead = ImageTk.PhotoImage(select_undead_button)

        self.button_image_select_trent_origin = Image.open("local_storage/shop_image/trent_button.png")
        select_trent_button = self.button_image_select_trent_origin.resize((295, 300))
        self.button_image_select_trent = ImageTk.PhotoImage(select_trent_button)

        self.button_image_select_human_origin = Image.open("local_storage/shop_image/human_button.png")
        select_human_button = self.button_image_select_human_origin.resize((295, 300))
        self.button_image_select_human = ImageTk.PhotoImage(select_human_button)

        self.button_image_back_to_lobby_origin = Image.open("local_storage/shop_image/lobby_button.png")
        back_to_lobby_button = self.button_image_back_to_lobby_origin.resize((220, 60))
        self.button_image_back_to_lobby = ImageTk.PhotoImage(back_to_lobby_button)

        self.button_image_my_card_origin = Image.open("local_storage/shop_image/my_card_button.png")
        my_card_button = self.button_image_my_card_origin.resize((220, 60))
        self.button_image_my_card_button = ImageTk.PhotoImage(my_card_button)

        # 전체 카드 선택
        self.get_new_all_cards_button = tkinter.Button(cardShopMenuFrame,
                                                       image=self.button_image_select_all,
                                                       bd=0, highlightthickness=0,
                                                       command=lambda: buy_check_button_click("전체"),
                                                       width=295, height=300)
        self.get_new_all_cards_button.place(relx=0.162, rely=0.53, anchor="center")


        # 언데드 카드 선택
        self.get_new_undead_cards_button = tkinter.Button(cardShopMenuFrame,
                                                          image=self.button_image_select_undead,
                                                          bd=0, highlightthickness=0,
                                                          command=lambda: buy_check_button_click("언데드"),
                                                          width=295, height=300)
        self.get_new_undead_cards_button.place(relx=0.39, rely=0.53, anchor="center")


        # 트랜트 카드 선택
        self.get_new_trant_cards_button = tkinter.Button(cardShopMenuFrame,
                                                         image=self.button_image_select_trent,
                                                         bd=0, highlightthickness=0,
                                                         command=lambda: buy_check_button_click("트랜트"),
                                                         width=295, height=300)
        self.get_new_trant_cards_button.place(relx=0.612, rely=0.53, anchor="center")


        # 휴먼 카드 선택
        self.get_new_human_cards_button = tkinter.Button(cardShopMenuFrame,
                                                         image=self.button_image_select_human,
                                                         bd=0, highlightthickness=0,
                                                         command=lambda: buy_check_button_click("휴먼"),
                                                         width=295, height=300)
        self.get_new_human_cards_button.place(relx=0.842, rely=0.53, anchor="center")

        # 로비로 돌아가기 버튼
        self.go_back_to_lobby_button = tkinter.Button(cardShopMenuFrame,
                                                      image=self.button_image_back_to_lobby,
                                                      bd=0, highlightthickness=0,
                                                      relief="flat",
                                                      command=lambda: switchFrameWithMenuName("lobby-menu"),
                                                      width=220, height=60)
        self.go_back_to_lobby_button.place(relx=0.058, rely=0.08, anchor="center")


        # 내 카드로 이동하는 버튼
        self.my_card_button = tkinter.Button(cardShopMenuFrame,
                                             image=self.button_image_my_card_button,
                                             bd=0, highlightthickness=0,
                                             relief="flat",
                                             command=lambda: onClickMyCard(),
                                             width=220, height=60)
        self.my_card_button.place(relx=0.058, rely=0.155, anchor="center")


        return cardShopMenuFrame


    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("CardShopMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__cardShopMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("CardShopMenuFrameServiceImpl: injectReceiveIpcChannel()")
        self.__cardShopMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)
