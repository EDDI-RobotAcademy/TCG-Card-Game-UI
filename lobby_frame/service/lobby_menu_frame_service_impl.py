import sys
import tkinter

from decouple import config

from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository as MuligunHandRepository
from battle_field_muligun.service.request.muligun_request import MuligunRequest
from battle_lobby_frame.controller.battle_lobby_frame_controller_impl import BattleLobbyFrameControllerImpl
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.request.request_deck_card_list import RequestDeckCardList
from battle_lobby_frame.service.request.request_deck_name_list_for_battle import RequestDeckNameListForBattle
from fake_battle_field.infra.fake_battle_field_frame_repository_impl import FakeBattleFieldFrameRepositoryImpl
from fake_battle_field.service.request.create_fake_battle_room_request import CreateFakeBattleRoomRequest
from lobby_frame.repository.lobby_menu_frame_repository_impl import LobbyMenuFrameRepositoryImpl
from lobby_frame.service.lobby_menu_frame_service import LobbyMenuFrameService
from lobby_frame.service.request.card_list_request import CardListRequest
from lobby_frame.service.request.check_game_money_request import CheckGameMoneyRequest
from matching_window.controller.matching_window_controller_impl import MatchingWindowControllerImpl
from lobby_frame.service.request.exit_request import ExitRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl


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
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.card_data_list = []

    def createLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        self.__switchFrameWithMenuName = switchFrameWithMenuName
        self.__rootWindow = rootWindow

        lobbyMenuFrame = self.__lobbyMenuFrameRepository.createLobbyMenuFrame(rootWindow)


        label_text = "EDDI TCG Card Battle"
        label = tkinter.Label(lobbyMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬

        battle_entrance_button = tkinter.Button(lobbyMenuFrame, text="대전 입장", bg="#2E2BE2", fg="white",
                                                width=36, height=2)
        battle_entrance_button.place(relx=0.5, rely=0.35, anchor="center")

        def onClickEntrance(event):
            #rootWindow.after(3000, self.__waitForPrepareBattle)
            self.__matchingWindowController.makeMatchingWindow(rootWindow)
            self.__matchingWindowController.matching(rootWindow)



        battle_entrance_button.bind("<Button-1>", onClickEntrance)

        my_card_button = tkinter.Button(lobbyMenuFrame, text="내 카드", bg="#2E2BE2", fg="white", width=36,
                                        height=2)
        my_card_button.place(relx=0.5, rely=0.5, anchor="center")

        card_shop_button = tkinter.Button(lobbyMenuFrame, text="상점", bg="#2E2BE2", fg="white",
                                          width=36, height=2)
        card_shop_button.place(relx=0.5, rely=0.65, anchor="center")

        exit_button = tkinter.Button(lobbyMenuFrame, text="종료", bg="#C62828", fg="white", width=36, height=2)
        exit_button.place(relx=0.5, rely=0.8, anchor="center")

        def on_fake_battle_field_button_click():
            print("Fake Battle Field Frame Start!")

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

                hand_card_list = deckCardListResponse['hand_card_list']
                print(f"hand card list: {hand_card_list}")

                # 위에 까지가 17번 완료
                # 19번 (가위 바위 보) -> 세션, "Rock"


                muligunResponseData = self.__muligunYourHandRepository.requestMuligun(
                    MuligunRequest(first_fake_redis_token,
                                   []))

                print(f"muligun responseData: {muligunResponseData}")
                self.__fakeYourHandRepository.save_current_hand_state(hand_card_list)

                deck_card_list = muligunResponseData['updated_deck_card_list']

                self.__fakeYourDeckRepository.save_deck_state(deck_card_list)

            switchFrameWithMenuName("fake-battle-field")

        fake_battle_field_button = tkinter.Button(lobbyMenuFrame, text="개발 테스트용 전장", bg="#2E2BE2", fg="white",
                                          # command=lambda: switchFrameWithMenuName("fake-battle-field"), width=36,
                                            command=on_fake_battle_field_button_click,
                                            width=36,
                                            height=2)
        fake_battle_field_button.place(relx=0.2, rely=0.65, anchor="center")

        def onClickExit(event):
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
            try:
                session_info = self.__sessionRepository.get_session_info()
                if session_info is not None:
                    responseData = self.__lobbyMenuFrameRepository.requestAccountCardList(
                        CardListRequest(session_info))

                    print(f"responseData: {responseData}")

                    if responseData is not None:
                        server_data = responseData.get("card_id_list")

                        for i, number in enumerate(server_data):
                            for key in server_data[i].keys():
                                self.card_data_list.append(int(key))
                                print(f"서버로 부터 카드 정보 잘 받았니?:{self.card_data_list}")

                        switchFrameWithMenuName("my-card-main")

                    else:
                        print("Invalid or missing response data.")

            except Exception as e:
                print(f"An error occurred: {e}")

        my_card_button.bind("<Button-1>", onClickMyCard)

        def onClickCardShop(event):
            try:
                responseData = self.__lobbyMenuFrameRepository.requestCheckGameMoney(CheckGameMoneyRequest
                                                                                     (self.__sessionRepository.get_session_info()))

                print(f"responseData: {responseData}")

                if responseData:
                    self.__cardShopFrameRepository.setMyMoney(responseData.get("account_point"))
                    from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import MyGameMoneyFrameServiceImpl
                    MyGameMoneyFrameServiceImpl.getInstance().findMyMoney()
                    switchFrameWithMenuName("card-shop-menu")
                    #switchFrameWithMenuName("rock-paper-scissors")
                else:
                    print("checkGameMoney responseData not found")

            except Exception as e:
                print(f"An error occurred: {e}")

        card_shop_button.bind("<Button-1>", onClickCardShop)

        return lobbyMenuFrame


    def get_card_data_list(self):
        return self.card_data_list

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
