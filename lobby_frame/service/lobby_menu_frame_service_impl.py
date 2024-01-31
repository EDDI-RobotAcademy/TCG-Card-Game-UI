import random
import time
import tkinter

from battle_lobby_frame.controller.battle_lobby_frame_controller_impl import BattleLobbyFrameControllerImpl
from battle_lobby_frame.service.request.request_deck_name_list_for_battle import RequestDeckNameListForBattle
from lobby_frame.repository.lobby_menu_frame_repository_impl import LobbyMenuFrameRepositoryImpl
from lobby_frame.service.lobby_menu_frame_service import LobbyMenuFrameService
from lobby_frame.service.request.cancel_matching_request import CancelMatchingRequest
from lobby_frame.service.request.check_matching_request import CheckMatchingRequest
from lobby_frame.service.request.check_prepare_battle_request import CheckPrepareBattleRequest
from lobby_frame.service.request.start_matching_request import StartMatchingRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from utility.image_generator import ImageGenerator


class LobbyMenuFrameServiceImpl(LobbyMenuFrameService):
    __instance = None
    __isMatching = None

    __switchFrameWithMenuName = None
    __rootWindow = None

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

    def __waitForPrepareBattle(self):
        print("LobbyMenuFrameServiceImpl: __waitForPrepareBattle()")
        while True:
            isPrepareCompleteResponse = self.__lobbyMenuFrameRepository.checkPrepareBattle(
                CheckPrepareBattleRequest(
                    self.__sessionRepository.get_session_info()
                )
            )
            currentStatus = isPrepareCompleteResponse.get("current_status")
            print(f"after request matching status: {currentStatus}")

            if currentStatus == "SUCCESS":
                self.__switchFrameWithMenuName("battle-lobby")
                break

            time.sleep(3)


    def createLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        self.__switchFrameWithMenuName = switchFrameWithMenuName
        self.__rootWindow = rootWindow

        lobbyMenuFrame = self.__lobbyMenuFrameRepository.createLobbyMenuFrame(rootWindow)
        imageGenerator = ImageGenerator.getInstance()

        label_text = "EDDI TCG Card Battle"
        label = tkinter.Label(lobbyMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.2, anchor="center", bordermode="outside")  # 가운데 정렬

        battle_entrance_button = tkinter.Button(lobbyMenuFrame, text="대전 입장", bg="#2E2BE2", fg="white",
                                                width=36, height=2)
        battle_entrance_button.place(relx=0.5, rely=0.35, anchor="center")

        def onClickEntrance(event):

            waitingWindow = tkinter.Frame(rootWindow, width=480, height=360)
            waitingWindow.place(relx=0.5, rely=0.5, anchor="center")
            waitingText = tkinter.Label(waitingWindow, text="매칭 시작!")
            waitingText.place(relx=0.5, rely=0.1, anchor="center")

            waitingBar = tkinter.Frame(waitingWindow, width=0, height=36, bg="#E22500")
            waitingBar.place(relx=0.5, rely=0.875, anchor="center")
            waitingPercent = tkinter.Label(waitingWindow)
            waitingPercent.place(relx=0.5, rely=0.96, anchor="center")

            # Todo : 마땅히 배치 할 곳이 없어서 잠시 안보이게 설정함
            waitingPercent.place_forget()

            imageWidth = 256
            imageHeight = 256
            waitingImage = tkinter.Canvas(waitingWindow, width=imageWidth, height=imageHeight)
            generatedImage = imageGenerator.getRandomCardImage()
            waitingImage.create_image(imageWidth/2, imageHeight/2, image=generatedImage)
            waitingImage.place(relx=0.5, rely=0.5, anchor="center", width=imageWidth, height=imageHeight)

            cancelMatchingButton = tkinter.Button(waitingWindow, text="매칭 취소")
            cancelMatchingButton.place(relx=0.5, rely=0.95, anchor="center")
            self.__isMatching = True
            def onClickCancelMatchingButton(event):
                matchingCancelResponse = self.__lobbyMenuFrameRepository.cancelMatching(
                    CancelMatchingRequest(
                        self.__sessionRepository.get_session_info()
                    )
                )
                if matchingCancelResponse is not None and matchingCancelResponse != "":
                    self.__isMatching = False
                    waitingWindow.destroy()

            cancelMatchingButton.bind("<Button-1>", onClickCancelMatchingButton)
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
                        if self.__isMatching:
                            generatedImage = imageGenerator.getRandomCardImage()
                            waitingImage.create_image(imageWidth / 2, imageHeight / 2, image=generatedImage)
                            #waitingImage.place(relx=0.5, rely=0.5, anchor="center", width=imageWidth, height=imageHeight)

                            isMatchingSuccessResponse = self.__lobbyMenuFrameRepository.checkMatching(
                                CheckMatchingRequest(
                                    self.__sessionRepository.get_session_info()
                                )
                            )
                            currentStatus = isMatchingSuccessResponse.get("current_status")
                            print(f"after request matching status: {currentStatus}")

                            if currentStatus == "FAIL":
                                waitingText.configure(text="매칭 실패!")
                                rootWindow.after(3000, lambda: waitingWindow.destroy)

                            if currentStatus == "WAIT":
                                waitingText.configure(text="매칭중입니다...")
                                rootWindow.after(3000, waitingForMatch)

                            if currentStatus == "PREPARE":
                                waitingText.configure(text="매칭 성공! 배틀 준비중입니다...")
                                self.__waitForPrepareBattle()

                            # else:
                            if currentStatus == "SUCCESS":
                                waitingText.configure(text="매칭 성공!")
                                waitingBar.place_forget()
                                waitingPercent.place_forget()
                                rootWindow.after(3000,
                                                 lambda: self.switchToBattleLobby(waitingWindow, switchFrameWithMenuName))

                    def update_width(i):
                        if self.__isMatching:
                            waitingBar.configure(width=i, height=9)
                            if i < 480:
                                rootWindow.after(10, lambda: update_width(i + (480 / 60 / 100)))
                                waitingPercent.configure(text=f"{round((i + (480 / 60 / 100)) / 480 * 100)}%")
                            else:
                                waitingWindow.destroy()



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

        #TODO 임시적으로 사용하는 버튼으로 나중에 battle 매칭 기능 완료되면 삭제 필요
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
