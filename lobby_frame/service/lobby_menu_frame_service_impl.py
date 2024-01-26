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
            try:
                afterBattleMatchResponse = self.__lobbyMenuFrameRepository.startMatch(
                    StartMatchingRequest(
                        self.__sessionRepository.readRedisTokenSessionInfoToFile()
                    )
                )

                is_success_to_insert_wait_queue = False

                if afterBattleMatchResponse:
                    is_success_to_insert_wait_queue = afterBattleMatchResponse.get("is_success")

                if is_success_to_insert_wait_queue:
                    while True:
                        isMatchingSuccessResponse = self.__lobbyMenuFrameRepository.checkMatching(
                            CheckMatchingRequest(
                                self.__sessionRepository.readRedisTokenSessionInfoToFile()
                            )
                        )

                        # print(f"isMatchingSuccessResponse: {isMatchingSuccessResponse}")
                        currentStatus = isMatchingSuccessResponse.get("current_status")
                        print(f"after request matching status: {currentStatus}")

                        if currentStatus == "FAIL":
                            print("배틀 매칭 실패!")
                            break
                        #else:
                        if currentStatus == "SUCCESS":
                            print("배틀 매칭 성공!")
                            # TODO: 배틀 필드 화면 그리면 연결해서 화면 전환 진행하세요
                            self.switchToBattleLobby(switchFrameWithMenuName)
                            break
                            #switchFrameWithMenuName("")

                        time.sleep(3)
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

        return lobbyMenuFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__lobbyMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__lobbyMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)



    def readyForMatching(self, switchFrameWithMenuName):
        try:
            isReadyForBattle = False
            while isReadyForBattle == False:
                readyResponse = self.__lobbyMenuFrameRepository.checkMatching(
                    CheckMatchingRequest(self.__sessionRepository.readRedisTokenSessionInfoToFile())
                )

                if readyResponse is not None and readyResponse != "":
                    isReadyForBattle = True
                    self.switchToBattleLobby(switchFrameWithMenuName)
                else:
                    time.sleep(3)


        except Exception as e:
            print(f"readyForMatching Error: {e}")

    def switchToBattleLobby(self, switchFrameWithMenuName):
        try:
            deckNameResponse = self.__lobbyMenuFrameRepository.requestDeckNameList(
                RequestDeckNameListForBattle(
                    self.__sessionRepository.readRedisTokenSessionInfoToFile()
                )
            )
            if deckNameResponse is not None and deckNameResponse != "":
                self.__battleLobbyFrameController.createDeckButtons(deckNameResponse)
                self.__battleLobbyFrameController.startCheckTime()
                switchFrameWithMenuName("battle-lobby")
        except Exception as e:
            print(f"switchToBattleLobby Error: {e}")