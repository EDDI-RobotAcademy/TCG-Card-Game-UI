import sys
import time
import tkinter
from PIL import ImageTk, Image
from colorama import Fore, Style

from decouple import config
from screeninfo import get_monitors

from battle_field.infra.opponent_field_energy_repository import OpponentFieldEnergyRepository
from battle_field.infra.opponent_hp_repository import OpponentHpRepository
from battle_field.infra.window_size_repository import WindowSizeRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_hp_repository import YourHpRepository
from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository as MuligunHandRepository
from battle_field_muligun.service.request.muligun_request import MuligunRequest
from battle_lobby_frame.controller.battle_lobby_frame_controller_impl import BattleLobbyFrameControllerImpl
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.request.request_deck_card_list import RequestDeckCardList
from battle_lobby_frame.service.request.request_deck_name_list_for_battle import RequestDeckNameListForBattle
from fake_battle_field.frame.fake_battle_field_frame import FakeBattleFieldFrame
from fake_battle_field.infra.fake_battle_field_frame_repository_impl import FakeBattleFieldFrameRepositoryImpl
from fake_battle_field.infra.fake_opponent_hand_repository import FakeOpponentHandRepositoryImpl
from fake_battle_field.service.request.create_fake_battle_room_request import CreateFakeBattleRoomRequest
from fake_battle_field.service.request.real_battle_start_request import RealBattleStartRequest
from lobby_frame.repository.lobby_menu_frame_repository_impl import LobbyMenuFrameRepositoryImpl
from lobby_frame.service.lobby_menu_frame_service import LobbyMenuFrameService
from lobby_frame.service.request.card_list_request import CardListRequest
from lobby_frame.service.request.check_game_money_request import CheckGameMoneyRequest
from matching_window.controller.matching_window_controller_impl import MatchingWindowControllerImpl
from lobby_frame.service.request.exit_request import ExitRequest
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl
from opengl_my_card_main_frame.infra.my_card_repository import MyCardRepository
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.repository.check_rock_paper_scissors_winner_repository_impl import \
    CheckRockPaperScissorsWinnerRepositoryImpl
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.service.check_rock_paper_scissors_winner_service_impl import \
    CheckRockPaperScissorsWinnerServiceImpl
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.service.request.check_rock_paper_scissors_winner_request import \
    CheckRockPaperScissorsWinnerRequest
from rock_paper_scissors.repository.rock_paper_scissors_repository import RockPaperScissorsRepository
from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl
from rock_paper_scissors.service.request.rock_paper_scissors_request import RockPaperScissorsRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from test_detector.detector import DetectorAboutTest

imageWidth = 256
imageHeight = 256


class LobbyMenuFrameServiceImpl(LobbyMenuFrameService):
    __instance = None
    __switchFrameWithMenuName = None
    __rootWindow = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__lobbyMenuFrameRepository = LobbyMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
            cls.__instance.__battleLobbyFrameController = BattleLobbyFrameControllerImpl.getInstance()
            cls.__instance.__matchingWindowController = MatchingWindowControllerImpl.getInstance()
            cls.__instance.__cardShopFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()

            # TODO: 이것은 Muligun 용 Hand를 사용하는 것으로 네이밍 이슈가 존재함 (변경 요망) -> MuligunYourHandRepository 권장
            cls.__instance.__muligunYourHandRepository = MuligunHandRepository.getInstance()
            cls.__instance.__fakeBattleFieldFrameRepository = FakeBattleFieldFrameRepositoryImpl.getInstance()

            # 이건 진짜 Hand를 Fake 용으로 사용하는 것
            # cls.__instance.__fakeYourHandRepository = YourHandRepository.getInstance()
            cls.__instance.__fakeYourHandRepository = YourHandRepository.getInstance()
            cls.__instance.__fakeYourDeckRepository = YourDeckRepository.getInstance()

            cls.__instance.__rockPaperScissorsRepositoryImpl = RockPaperScissorsRepositoryImpl.getInstance()
            cls.__instance.__checkRockPaperScissorsWinnerServiceImpl = CheckRockPaperScissorsWinnerServiceImpl.getInstance()
            cls.__instance.__checkRockPaperScissorsWinnerRepositoryImpl = CheckRockPaperScissorsWinnerRepositoryImpl.getInstance()

            cls.__instance.__fakeOpponentHandRepository = FakeOpponentHandRepositoryImpl.getInstance()
            cls.__instance.__notify_reader_repository = NotifyReaderRepositoryImpl.getInstance()

            cls.__instance.__yourFieldEnergyRepository = YourFieldEnergyRepository.getInstance()
            cls.__instance.__opponentFieldEnergyRepository = OpponentFieldEnergyRepository.getInstance()

            cls.__instance.__windowSizeRepository = WindowSizeRepository.getInstance()
            cls.__instance.__yourHpRepository = YourHpRepository.getInstance()
            cls.__instance.__opponentHpRepository = OpponentHpRepository.getInstance()

            # Shop
            cls.__instance.__myCardRepository = MyCardRepository.getInstance()
            cls.__instance.__musicPlayerRepository = MusicPlayerRepositoryImpl.getInstance()

            # Fake Battle Field
            cls.__instance.__detector_about_test = DetectorAboutTest.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.card_data_list = []
        self.number_of_cards_list = []

    def createLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        self.__switchFrameWithMenuName = switchFrameWithMenuName
        self.__rootWindow = rootWindow

        # 이미지 버튼의 크기에 맞게 resize
        self.button_image_ent_game_origin = Image.open("local_storage/image/battle_lobby/entrance_game_button.png")
        ent_game_button = self.button_image_ent_game_origin.resize((850, 99))
        self.button_image_ent_game = ImageTk.PhotoImage(ent_game_button)

        self.button_image_my_card_origin = Image.open("local_storage/image/battle_lobby/my_card_button.png")
        my_card_button = self.button_image_my_card_origin.resize((850, 99))
        self.button_image_my_card = ImageTk.PhotoImage(my_card_button)

        self.button_image_shop_origin = Image.open("local_storage/image/battle_lobby/shop_button.png")
        shop_button = self.button_image_shop_origin.resize((850, 99))
        self.button_image_shop = ImageTk.PhotoImage(shop_button)

        self.button_image_exit_origin = Image.open("local_storage/image/battle_lobby/exit_button.png")
        exit_button = self.button_image_exit_origin.resize((850, 99))
        self.button_image_exit = ImageTk.PhotoImage(exit_button)

        self.button_image_test_game_origin = Image.open("local_storage/image/battle_lobby/test_button.png")
        test_button = self.button_image_test_game_origin.resize((850, 99))
        self.button_image_test_game = ImageTk.PhotoImage(test_button)


        lobbyMenuFrame = self.__lobbyMenuFrameRepository.createLobbyMenuFrame(rootWindow)


        # label_text = "EDDI TCG Card Battle"
        # label = tkinter.Label(lobbyMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
        #                       anchor="center", justify="center", pady=50)
        #
        # label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬

        # 대전 입장 버튼
        battle_entrance_button = tkinter.Button(lobbyMenuFrame,
                                                image=self.button_image_ent_game, bd=0, highlightthickness=0,
                                                width=850, height=99)
        battle_entrance_button.place(relx=0.32, rely=0.355, anchor="center")

        def onClickEntrance(event):
            #rootWindow.after(3000, self.__waitForPrepareBattle)
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')

            self.__sessionRepository.clearFirstFakeSessionInfoFile()
            self.__detector_about_test.set_is_fake_battle_field(False)

            self.__matchingWindowController.makeMatchingWindow(rootWindow)
            self.__matchingWindowController.matching(rootWindow)


        battle_entrance_button.bind("<Button-1>", onClickEntrance)


        # 내 카드 버튼
        my_card_button = tkinter.Button(lobbyMenuFrame,
                                        image=self.button_image_my_card, bd=0, highlightthickness=0,
                                        width=850, height=99)
        my_card_button.place(relx=0.32, rely=0.495, anchor="center")


        # 상점 버튼
        card_shop_button = tkinter.Button(lobbyMenuFrame,
                                          image=self.button_image_shop, bd=0, highlightthickness=0,
                                          width=850, height=99)
        card_shop_button.place(relx=0.32, rely=0.64, anchor="center")

        # 종료 버튼
        exit_button = tkinter.Button(lobbyMenuFrame,
                                     image=self.button_image_exit, bd=0, highlightthickness=0,
                                     width=850, height=99)
        exit_button.place(relx=0.32, rely=0.783, anchor="center")

        def on_fake_battle_field_button_click():
            print("Fake Battle Field Frame Start!")
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')

            create_fake_battle_field_response = self.__fakeBattleFieldFrameRepository.requestCreateFakeBattleRoom(
                CreateFakeBattleRoomRequest())

            print("Fake Battle Field Frame Response:", create_fake_battle_field_response)

            if create_fake_battle_field_response:
                first_fake_redis_token = create_fake_battle_field_response.get("first_fake_session")
                second_fake_redis_token = create_fake_battle_field_response.get("second_fake_session")

                if first_fake_redis_token is not None and isinstance(first_fake_redis_token, str) and first_fake_redis_token != "":
                    print(f"First Fake redis_token received: {first_fake_redis_token}")

                    self.__sessionRepository.writeFirstFakeRedisTokenSessionInfoToFile(first_fake_redis_token)

                if second_fake_redis_token is not None and isinstance(second_fake_redis_token, str) and second_fake_redis_token != "":
                    print(f"Second Fake redis_token received: {second_fake_redis_token}")

                    self.__sessionRepository.writeSecondFakeRedisTokenSessionInfoToFile(second_fake_redis_token)

                deckNameResponse = self.__fakeBattleFieldFrameRepository.request_deck_name_list_for_fake_battle(
                    RequestDeckNameListForBattle(
                        first_fake_redis_token
                    )
                )
                if deckNameResponse is None or deckNameResponse == "":
                    print("Fake Battle Room 테스트를 위한 기본 설정을 먼저 진행하세요!")

                print(f"deck name response: {deckNameResponse}")

                deckCardListResponse = self.__fakeBattleFieldFrameRepository.request_card_list(
                    # 덱 Id 값을 Fake Test 목적으로 만든 숫자에 맞춰야함
                    RequestDeckCardList(config('FAKE_DECK_ID'),
                                        first_fake_redis_token)
                )

                print(f"deckCardListResponse: {deckCardListResponse}")
                if deckCardListResponse is None or deckCardListResponse == "":
                    print("Fake Battle Room 테스트를 위한 기본 설정을 먼저 진행하세요!")

                your_hand_card_list = deckCardListResponse['hand_card_list']
                print(f"your_hand card list: {your_hand_card_list}")

                # 위에 까지가 Your 17번 완료

                # Opponent 17 번
                deckNameResponse = self.__fakeBattleFieldFrameRepository.request_deck_name_list_for_fake_battle(
                    RequestDeckNameListForBattle(
                        second_fake_redis_token
                    )
                )

                deckCardListResponse = self.__fakeBattleFieldFrameRepository.request_card_list(
                    # 덱 Id 값을 Fake Test 목적으로 만든 숫자에 맞춰야함
                    RequestDeckCardList(config('FAKE_DECK_ID'),
                                        second_fake_redis_token)
                )

                opponent_hand_card_list = deckCardListResponse['hand_card_list']
                print(f"opponent_hand card list: {opponent_hand_card_list}")

                # 19번 (가위 바위 보) -> 세션, "Rock"

                responseData = self.__rockPaperScissorsRepositoryImpl.requestRockPaperScissors(
                    RockPaperScissorsRequest(self.__sessionRepository.get_first_fake_session_info(), "Rock"))

                print(f"First Fake Accounts (가위 바위 보) -> responseData: {responseData}")

                responseData = self.__rockPaperScissorsRepositoryImpl.requestRockPaperScissors(
                    RockPaperScissorsRequest(self.__sessionRepository.get_second_fake_session_info(), "Scissors"))

                print(f"Second Fake Accounts (가위 바위 보) -> responseData: {responseData}")

                while True:
                    responseData = self.__checkRockPaperScissorsWinnerRepositoryImpl.requestCheckRockPaperScissorsWinner(
                        CheckRockPaperScissorsWinnerRequest(self.__sessionRepository.get_first_fake_session_info()))
                    print(f"First Fake Accounts (가위 바위 보 결과) responseData: {responseData}")

                    result = responseData['am_i_first_turn']

                    if result == "WAIT":
                        pass

                    elif result == "WIN" or result == "LOSE":
                        break

                    time.sleep(1)

                while True:
                    responseData = self.__checkRockPaperScissorsWinnerRepositoryImpl.requestCheckRockPaperScissorsWinner(
                        CheckRockPaperScissorsWinnerRequest(self.__sessionRepository.get_second_fake_session_info()))
                    print(f"Second Fake Accounts (가위 바위 보 결과) responseData: {responseData}")

                    result = responseData['am_i_first_turn']

                    if result == "WAIT":
                        pass

                    elif result == "WIN" or result == "LOSE":
                        break

                    time.sleep(1)

                # First Fake Accounts (Your)
                yourMuligunResponseData = self.__muligunYourHandRepository.requestMuligun(
                    MuligunRequest(first_fake_redis_token,
                                   []))

                print(f"muligun responseData: {yourMuligunResponseData}")
                self.__fakeYourHandRepository.save_current_hand_state(your_hand_card_list)

                deck_card_list = yourMuligunResponseData['updated_deck_card_list']

                # Second Fake Accounts (Opponent)
                opponentMuligunResponseData = self.__muligunYourHandRepository.requestMuligun(
                    MuligunRequest(second_fake_redis_token,
                                   []))

                print(f"muligun responseData: {opponentMuligunResponseData}")

                self.__fakeYourDeckRepository.save_deck_state(deck_card_list)

                # First Fake Accounts (Your) Real Battle Start
                real_battle_start_response = self.__fakeBattleFieldFrameRepository.request_real_battle_start(
                    RealBattleStartRequest(first_fake_redis_token)
                )
                print(f"your real_battle_start_response: {real_battle_start_response}")

                is_your_turn_value = real_battle_start_response.get('is_your_turn', None)
                print(f"{Fore.RED}is_your_turn_value: {is_your_turn_value}{Style.RESET_ALL}")
                self.__notify_reader_repository.set_is_your_turn_for_check_fake_process(is_your_turn_value)

                your_draw_card_id = real_battle_start_response.get('player_draw_card_list_map', {}).get('You', [])[0]
                print(f"your_draw_card_id: {your_draw_card_id}")

                self.__fakeYourHandRepository.save_current_hand_state([your_draw_card_id])
                current_hand_card_list = self.__fakeYourHandRepository.get_current_hand_state()
                print(f"{Fore.RED} current_hand_card_list: {current_hand_card_list}{Style.RESET_ALL}")

                if self.__windowSizeRepository.get_is_it_re_entrance():
                    print(f"{Fore.RED} get_is_it_re_entrance(): {self.__windowSizeRepository.get_is_it_re_entrance()}{Style.RESET_ALL}")
                    total_width = self.__windowSizeRepository.get_total_width()
                    total_height = self.__windowSizeRepository.get_total_height()

                    get_master_opengl_frame = self.__windowSizeRepository.get_master_opengl_frame()
                    get_master_opengl_frame.init_first_window(total_width, total_height)

                    self.__yourHpRepository.set_first_hp_state()
                    self.__opponentHpRepository.set_first_hp_state()

                #     self.__fakeYourHandRepository.set_total_window_size(total_width, total_height)
                #     self.__fakeYourHandRepository.update_your_hand()
                #
                #     self.__fakeYourDeckRepository.set_total_window_size(total_width, total_height)
                #     self.__fakeYourDeckRepository.update_deck(deck_card_list)

                self.__fakeYourDeckRepository.get_current_deck_state_object().draw_card()

                your_field_energy = real_battle_start_response['player_field_energy_map']['You']
                print(f"your_field_energy: {your_field_energy}")

                self.__yourFieldEnergyRepository.increase_your_field_energy(your_field_energy)

                # Second Fake Accounts (Your) Real Battle Start
                real_battle_start_response = self.__fakeBattleFieldFrameRepository.request_real_battle_start(
                    RealBattleStartRequest(second_fake_redis_token)
                )
                print(f"opponent real_battle_start_response: {real_battle_start_response}")

                if self.__windowSizeRepository.get_is_it_re_entrance():
                    self.__fakeOpponentHandRepository.clear_fake_opponent_hand_list()
                    self.__fakeOpponentHandRepository.save_fake_opponent_hand_list(opponent_hand_card_list)
                else:
                    self.__fakeOpponentHandRepository.save_fake_opponent_hand_list(opponent_hand_card_list)

                opponent_field_energy = real_battle_start_response['player_field_energy_map']['Opponent']
                print(f"opponent_field_energy: {opponent_field_energy}")

                self.__opponentFieldEnergyRepository.increase_opponent_field_energy(opponent_field_energy)
                self.__detector_about_test.set_is_fake_battle_field(True)

            switchFrameWithMenuName("fake-battle-field")

        fake_battle_field_button = tkinter.Button(lobbyMenuFrame, text="개발 테스트용 전장", bg="#2E2BE2", fg="white",
                                          # command=lambda: switchFrameWithMenuName("fake-battle-field"), width=36,
                                            command=on_fake_battle_field_button_click,
                                            width=36,
                                            height=2)
        fake_battle_field_button.place(relx=0.2, rely=0.65, anchor="center")

        def onClickExit(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')
            try:
                responseData = self.__lobbyMenuFrameRepository.requestProgramExit(
                    ExitRequest())

                print(f"responseData: {responseData}")

                if responseData and responseData.get("does_client_exit_success") is True:
                    rootWindow.destroy()
                    sys.exit()
                else:
                    print("응답이 잘못 되었음")
            except Exception as e:
                print(f"An error occurred: {e}")

        exit_button.bind("<Button-1>", onClickExit)

        def onClickMyCard(event):
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

        my_card_button.bind("<Button-1>", onClickMyCard)

        def onClickCardShop(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')
            try:
                responseData = self.__lobbyMenuFrameRepository.requestCheckGameMoney(CheckGameMoneyRequest
                                                                                     (self.__sessionRepository.get_session_info()))

                print(f"responseData: {responseData}")

                if responseData:
                    self.__cardShopFrameRepository.setMyMoney(responseData.get("account_point"))
                    from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import MyGameMoneyFrameServiceImpl
                    MyGameMoneyFrameServiceImpl.getInstance().findMyMoney()
                    switchFrameWithMenuName("card-shop-menu")
                else:
                    print("checkGameMoney responseData not found")

            except Exception as e:
                print(f"An error occurred: {e}")

        card_shop_button.bind("<Button-1>", onClickCardShop)

        def play_mouse_on_button_sound(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('mouse_on_button')

        battle_entrance_button.bind("<Enter>", play_mouse_on_button_sound)
        fake_battle_field_button.bind("<Enter>", play_mouse_on_button_sound)
        my_card_button.bind("<Enter>", play_mouse_on_button_sound)
        card_shop_button.bind("<Enter>", play_mouse_on_button_sound)
        exit_button.bind("<Enter>", play_mouse_on_button_sound)

        return lobbyMenuFrame

    def get_card_data_list(self):
        return self.card_data_list

    def get_number_of_cards_list(self):
        return self.number_of_cards_list

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__lobbyMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__lobbyMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)

    def switchToBattleLobby(self, windowToDestroy):
        windowToDestroy.destroy()
        try:
            deckNameResponse = self.__battleLobbyFrameRepository.requestDeckNameList(
                RequestDeckNameListForBattle(
                    self.__sessionRepository.get_session_info()
                )
            )
            if deckNameResponse is not None and deckNameResponse != "":
                print(f"switchToBattleLobby : 호출됨 {deckNameResponse}")
               # BattleFieldRepository.getInstance().start_game()
                self.__battleLobbyFrameController.startCheckTime()
                self.__battleLobbyFrameController.createDeckButtons(deckNameResponse, self.__switchFrameWithMenuName)
                self.__switchFrameWithMenuName("battle-lobby")
        except Exception as e:
            print(f"switchToBattleLobby Error: {e}")
