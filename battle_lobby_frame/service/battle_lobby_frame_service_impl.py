import tkinter

from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_frame_service import BattleLobbyFrameService


# from discarded.battle_room_list_frame.repository import BattleRoomListFrameRepositoryImpl


class BattleLobbyFrameServiceImpl(BattleLobbyFrameService):
    __instance = None
    __battleLobbyFrame = None
    __onClickEventList = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
        #  cls.__instance.__battleRoomListFrameRepository = BattleRoomListFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        self.__battleLobbyFrame = self.__battleLobbyFrameRepository.createBattleLobbyFrame(rootWindow)

        # list_scroll = tkinter.Frame(battleLobbyFrame)

        # battle_menu_frame = tkinter.Frame(battleLobbyFrame, width=MENU_WIDTH, height=SCREEN_HEIGHT, bg="#003333")
        # battle_menu_frame.pack(side="right")
        # def on_list_scroll_up(event):
        #     try:
        #         # responseData = self.__accountRegisterFrameRepository.requestRegister(
        #         #     AccountRegisterRequest(entry_username.get(), entry_password.get()))
        #
        #         print(f"responseData: {123123}")
        #
        #         # if responseData and responseData.get("is_success") is True:
        #         #     switchFrameWithMenuName("login-menu")
        #         # else:
        #         #     print("Invalid or missing response data.")
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        #
        # def on_list_scroll_down(event):
        #     try:
        #         # responseData = self.__accountRegisterFrameRepository.requestRegister(
        #         #     AccountRegisterRequest(entry_username.get(), entry_password.get()))
        #
        #         print(f"responseData: {456456456}")
        #         self.__battleRoomListFrameRepository.createBattleRoomListFrame(list_scroll,
        #                                                                        request=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        #
        #         # if responseData and responseData.get("is_success") is True:
        #         #     switchFrameWithMenuName("login-menu")
        #         # else:
        #         #     print("Invalid or missing response data.")
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        #
        # def on_list_scroll(event):
        #     try:
        #         # responseData = self.__accountRegisterFrameRepository.requestRegister(
        #         #     AccountRegisterRequest(entry_username.get(), entry_password.get()))
        #
        #         print(f"responseData: aasdfasdfasdf")
        #
        #         # if responseData and responseData.get("is_success") is True:
        #         #     switchFrameWithMenuName("login-menu")
        #         # else:
        #         #     print("Invalid or missing response data.")
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        #
        # list_scroll.bind("<Button-4>", on_list_scroll_up)
        # list_scroll.bind("<Button-5>", on_list_scroll_down)
        #
        # list_scroll.place(relx=0.1, rely=0.325,  relwidth=0.63, relheight=0.6)

        # # label_text = "GET READY FOR THE NEXT BATTLE"
        # # label = tkinter.Label(battleLobbyFrame, text=label_text, font=("Helvetica", 50), bg="black", fg="white",
        # #                       anchor="center", justify="center", pady=50)
        # #
        # # label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬
        #
        # battle_menu_frame = tkinter.Frame(battleLobbyFrame, width=MENU_WIDTH, height=SCREEN_HEIGHT, bg="#003333")
        # battle_menu_frame.pack(side="right")
        #
        # battle_menu_border = tkinter.Frame(battleLobbyFrame, width=BORDER_WIDTH, height=SCREEN_HEIGHT, bg="#CCFF33")
        # battle_menu_border.pack(side="right")
        #
        # battle_room_list_frame = tkinter.Frame(battleLobbyFrame, width=LIST_WIDTH, height=SCREEN_HEIGHT, bg="#000000")
        # battle_room_list_frame.pack(side="left")
        #
        # #
        # # battle_entrance_button = tkinter.Button(battleLobbyMenuFrame, text="대전 입장", bg="#2E2BE2", fg="white",
        # #                                         command=lambda: switchFrameWithMenuName("login-menu"), width=36,
        # #                                         height=2)
        # # battle_entrance_button.place(relx=0.5, rely=0.35, anchor="center")
        # #
        # # my_card_button = tkinter.Button(battleLobbyMenuFrame, text="내 카드", bg="#2E2BE2", fg="white",
        # #                                 command=lambda: switchFrameWithMenuName("my-card"), width=36,
        # #                                 height=2)
        # # my_card_button.place(relx=0.5, rely=0.5, anchor="center")
        # #
        # # card_shop_button = tkinter.Button(battleLobbyMenuFrame, text="상점", bg="#2E2BE2", fg="white",
        # #                                   command=lambda: switchFrameWithMenuName("card-shop-menu"), width=36,
        # #                                   height=2)
        # # card_shop_button.place(relx=0.5, rely=0.65, anchor="center")
        # #
        # # exit_button = tkinter.Button(battleLobbyMenuFrame, text="종료", bg="#C62828", fg="white",
        # #                              command=battleLobbyMenuFrame.quit, width=36, height=2)
        # # exit_button.place(relx=0.5, rely=0.8, anchor="center")

        label = tkinter.Label(self.__battleLobbyFrame, text="WATING ROOM FOR BATTLE", font=("Helvetica", 50, "bold"),
                              fg="#FFFFFF", bg="#000000")
        label.place(relx=0.5, rely=0.15, anchor="center")

        # TODO: 테스트코드지워야함
        request = [{'deckName': "ㅁㄴㅇㄻㄴㅇㄹ"}, {'deckName': "123123"}, {'deckName': "568567858"}, {'deckName': "ㅋㅋㅋㅋㅋㅋㅋ"},
                   {'deckName': "ㅋ시발 "}, {'deckName': "되냐??"}]

        self.createBattleLobbyMyDeckButton(request)

        enterButton = tkinter.Button(self.__battleLobbyFrame, text="입장", font=("Arial", 20))
        enterButton.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.15, relheight=0.075)

        return self.__battleLobbyFrame

    def createBattleLobbyMyDeckButton(self, request=None):
        if request:
            def relX(j):
                return 0.3 if j % 2 == 0 else 0.7

            for i, deckData in enumerate(request):
                deck = tkinter.Label(self.__battleLobbyFrame, text=f"{deckData['deckName']}", font=("Helvetica", 15))
                deck.place(relx=relX(i), rely=0.4 + (i // 2 * 0.15),
                           anchor="center", relwidth=0.25, relheight=0.1)

                def onClick(event, _deck: tkinter.Button):
                    self.__battleLobbyFrameRepository.selectDeck(_deck)

                deck.bind("<Button-1>", lambda event, current_deck=deck: onClick(event, current_deck))
                self.__battleLobbyFrameRepository.addDeckToDeckList(deck)
