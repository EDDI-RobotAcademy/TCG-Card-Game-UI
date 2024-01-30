import time
import tkinter

from battle_lobby_frame.controller.battle_lobby_frame_controller_impl import BattleLobbyFrameControllerImpl
from battle_lobby_frame.service.request.request_deck_name_list_for_battle import RequestDeckNameListForBattle
from lobby_frame.repository.lobby_menu_frame_repository_impl import LobbyMenuFrameRepositoryImpl
from lobby_frame.service.lobby_menu_frame_service import LobbyMenuFrameService
from lobby_frame.service.request.check_matching_request import CheckMatchingRequest
from lobby_frame.service.request.start_matching_request import StartMatchingRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class LobbyMenuFrameServiceImpl(LobbyMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__lobbyMenuFrameRepository = LobbyMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__battleLobbyFrameController = BattleLobbyFrameControllerImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        lobbyMenuFrame = self.__lobbyMenuFrameRepository.createLobbyMenuFrame(rootWindow)

        label_text = "EDDI TCG Card Battle"
        label = tkinter.Label(lobbyMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬

        battle_entrance_button = tkinter.Button(lobbyMenuFrame, text="대전 입장", bg="#2E2BE2", fg="white",
                                                width=36, height=2)
        battle_entrance_button.place(relx=0.5, rely=0.35, anchor="center")

        def onClickEntrance(event):

            watingWindow = tkinter.Frame(rootWindow, width=480, height=360)
            watingWindow.place(relx=0.5, rely=0.5, anchor="center")
            watingText = tkinter.Label(watingWindow, text="매칭 시작!")
            watingText.place(relx=0.5, rely=0.5, anchor="center")

            watingBar = tkinter.Frame(watingWindow, width=0, height=36, bg="#E22500")
            watingBar.place(relx=0.5, rely=0.9, anchor="center")
            watingPercent = tkinter.Label(watingWindow)
            watingPercent.place(relx=0.5, rely=0.8, anchor="center")
            rootWindow.update()

            try:
                afterBattleMatchResponse = self.__lobbyMenuFrameRepository.startMatch(
                    StartMatchingRequest(
                        self.__sessionRepository.get_session_info()
                    )
                )

                is_success_to_insert_wait_queue = False

                if afterBattleMatchResponse:
                    is_success_to_insert_wait_queue = afterBattleMatchResponse.get("is_success")

                if is_success_to_insert_wait_queue:
                    def waitingForMatch():
                        isMatchingSuccessResponse = self.__lobbyMenuFrameRepository.checkMatching(
                            CheckMatchingRequest(
                                self.__sessionRepository.get_session_info()
                            )
                        )
                        currentStatus = isMatchingSuccessResponse.get("current_status")
                        print(f"after request matching status: {currentStatus}")

                        if currentStatus == "FAIL":
                            watingText.configure(text="매칭 실패!")
                            rootWindow.after(3000, lambda: watingWindow.destroy)

                        if currentStatus == "WAIT":
                            watingText.configure(text="매칭중입니다...")
                            rootWindow.after(3000, waitingForMatch)

                        # else:
                        if currentStatus == "SUCCESS":
                            watingText.configure(text="매칭 성공!")
                            watingBar.place_forget()
                            watingPercent.place_forget()
                            rootWindow.after(3000, lambda: self.switchToBattleLobby(watingWindow, switchFrameWithMenuName))



                    def update_width(i):
                        watingBar.configure(width=i, height=36)
                        if i<480:
                            rootWindow.after(10, lambda: update_width(i + (480/60/100)))
                            watingPercent.configure(text = f"{round((i + (480/60/100))/480*100)}%")
                        else:
                            watingWindow.destroy()

                    update_width(0)
                    rootWindow.after(3000, waitingForMatch)

                else:
                    print("Invalid or missing response data.")

            except Exception as e:
                print(f"onClickEntrance Error: {e}")

        battle_entrance_button.bind("<Button-1>", onClickEntrance)

        my_card_button = tkinter.Button(lobbyMenuFrame, text="내 카드", bg="#2E2BE2", fg="white",
                                        command=lambda: switchFrameWithMenuName("my-card-main"), width=36,
                                        height=2)
        my_card_button.place(relx=0.5, rely=0.5, anchor="center")

        card_shop_button = tkinter.Button(lobbyMenuFrame, text="상점", bg="#2E2BE2", fg="white",
                                          command=lambda: switchFrameWithMenuName("card-shop-menu"), width=36,
                                          height=2)
        card_shop_button.place(relx=0.5, rely=0.65, anchor="center")

        exit_button = tkinter.Button(lobbyMenuFrame, text="종료", bg="#C62828", fg="white",
                                     command=lobbyMenuFrame.quit, width=36, height=2)
        exit_button.place(relx=0.5, rely=0.8, anchor="center")

        battle_field_button = tkinter.Button(lobbyMenuFrame, text="전장으로", bg="#2E2BE2", fg="white",
                                          command=lambda: switchFrameWithMenuName("battle-field"), width=20,
                                          height=2)
        battle_field_button.place(relx=0.1, rely=0.65, anchor="center")

        return lobbyMenuFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__lobbyMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__lobbyMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)


    def switchToBattleLobby(self, windowToDestory, switchFrameWithMenuName):
        try:
            windowToDestory.place_forget()
            deckNameResponse = self.__lobbyMenuFrameRepository.requestDeckNameList(
                RequestDeckNameListForBattle(
                    self.__sessionRepository.get_session_info()
                )
            )
            if deckNameResponse is not None and deckNameResponse != "":
                print(f"switchToBattleLobby : 호출됨 {deckNameResponse}")
                self.__battleLobbyFrameController.startCheckTime()
                self.__battleLobbyFrameController.createDeckButtons(deckNameResponse, switchFrameWithMenuName)
                switchFrameWithMenuName("battle-lobby")
        except Exception as e:
            print(f"switchToBattleLobby Error: {e}")