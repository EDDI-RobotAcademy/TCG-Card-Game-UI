import tkinter

from battle_lobby_frame.repository.battle_lobby_menu_frame_repository_impl import BattleLobbyMenuFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_menu_frame_service import BattleLobbyMenuFrameService


class BattleLobbyMenuFrameServiceImpl(BattleLobbyMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleLobbyMenuFrameRepository = BattleLobbyMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance
    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        battleLobbyMenuFrame = self.__battleLobbyMenuFrameRepository.createBattleLobbyMenuFrame(rootWindow)

        label_text = "GET READY FOR THE NEXT BATTLE"
        label = tkinter.Label(battleLobbyMenuFrame, text=label_text, font=("Helvetica", 50), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬
        #
        # battle_entrance_button = tkinter.Button(battleLobbyMenuFrame, text="대전 입장", bg="#2E2BE2", fg="white",
        #                                         command=lambda: switchFrameWithMenuName("login-menu"), width=36,
        #                                         height=2)
        # battle_entrance_button.place(relx=0.5, rely=0.35, anchor="center")
        #
        # my_card_button = tkinter.Button(battleLobbyMenuFrame, text="내 카드", bg="#2E2BE2", fg="white",
        #                                 command=lambda: switchFrameWithMenuName("my-card"), width=36,
        #                                 height=2)
        # my_card_button.place(relx=0.5, rely=0.5, anchor="center")
        #
        # card_shop_button = tkinter.Button(battleLobbyMenuFrame, text="상점", bg="#2E2BE2", fg="white",
        #                                   command=lambda: switchFrameWithMenuName("card-shop-menu"), width=36,
        #                                   height=2)
        # card_shop_button.place(relx=0.5, rely=0.65, anchor="center")
        #
        # exit_button = tkinter.Button(battleLobbyMenuFrame, text="종료", bg="#C62828", fg="white",
        #                              command=battleLobbyMenuFrame.quit, width=36, height=2)
        # exit_button.place(relx=0.5, rely=0.8, anchor="center")

        return battleLobbyMenuFrame
