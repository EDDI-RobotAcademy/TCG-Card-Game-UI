import time
import tkinter

from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from matching_window.repository.matching_window_repository_impl import MatchingWindowRepositoryImpl
from matching_window.service.matching_window_service import MatchingWindowService
from matching_window.service.request.cancel_matching_request import CancelMatchingRequest
from matching_window.service.request.check_matching_request import CheckMatchingRequest
from matching_window.service.request.check_prepare_battle_request import CheckPrepareBattleRequest
from matching_window.service.request.room_number_request import RoomNumberRequest
from matching_window.service.request.start_matching_request import StartMatchingRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from utility.image_generator import ImageGenerator


imageWidth = 256
imageHeight = 256


class MatchingWindowServiceImpl(MatchingWindowService):
    __instance = None
    __isRoomPrepared = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__matchingWindowRepository = MatchingWindowRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __waitForPrepareBattle(self):
        while True:
            print("LobbyMenuFrameServiceImpl: __waitForPrepareBattle()")
            isPrepareCompleteResponse = self.__matchingWindowRepository.checkPrepareBattle(
                CheckPrepareBattleRequest(
                    self.__sessionRepository.get_session_info()
                )
            )
            currentStatus = isPrepareCompleteResponse.get("current_status")
            print(f"after request matching status: {currentStatus}")

            if currentStatus == "SUCCESS":
                print(f"server is prepared!!")
                break
            else:
                time.sleep(3)

    def __saveRoomNumber(self):
        try:
            roomNumberResponse = self.__matchingWindowRepository.requestRoomNumber(
                RoomNumberRequest(self.__sessionRepository.get_session_info())
            )
            print(f"room number: {roomNumberResponse}")
            roomNumber = roomNumberResponse.get("room_number")
            BattleFieldFunctionRepositoryImpl.getInstance().saveRoomNumber(roomNumber)
        except Exception as e:
            print(f"roomNumberError: {e}")
    def createMatchingWindow(self, rootWindow):
        self.__matchingWindow = self.__matchingWindowRepository.createMatchingWindowFrame(rootWindow)

        # self.__imageGenerator = ImageGenerator.getInstance()
        # matchingWindow.configure(width=480, height=360)
        # matchingWindow.place(relx=0.5, rely=0.5, anchor="center")
        #
        # matchingText = tkinter.Label(master=matchingWindow, text="매칭 시작!")
        # matchingText.place(relx=0.5, rely=0.1, anchor="center")
        #
        # matchingBar = tkinter.Frame(master=matchingWindow, width=0, height=36, bg="#E22500")
        # matchingBar.place(relx=0.5, rely=0.875, anchor="center")
        #
        # waitingImage = tkinter.Canvas(master=matchingWindow, width=imageWidth, height=imageHeight)
        # generatedImage = self.__imageGenerator.getRandomCardImage()
        # waitingImage.create_image(imageWidth / 2, imageHeight / 2, image=generatedImage)
        # waitingImage.place(relx=0.5, rely=0.5, anchor="center", width=imageWidth, height=imageHeight)
        #
        # cancelMatchingButton = tkinter.Button(master=matchingWindow, text="매칭 취소")
        # cancelMatchingButton.place(relx=0.5, rely=0.95, anchor="center")
        # self.__isMatching = True
        # matchingPercent = tkinter.Label(matchingWindow)
        # matchingPercent.place(relx=0.5, rely=0.96, anchor="center")

        def onClickCancelMatchingButton(event):
            matchingCancelResponse = self.__matchingWindowRepository.cancelMatching(
                CancelMatchingRequest(
                    self.__sessionRepository.get_session_info()
                )
            )
            if matchingCancelResponse is not None and matchingCancelResponse != "":
                self.matchingCancel()


        self.__matchingWindow.getCancelMatchingButton().bind("<Button-1>", onClickCancelMatchingButton)
        rootWindow.update()

    def startMatching(self, rootWindow):
        self.__isMatching = True
        try:
            startMatchResponse = self.__matchingWindowRepository.requestMatching(
                StartMatchingRequest(
                    self.__sessionRepository.get_session_info()
                )
            )
            print(f"startMatching: {startMatchResponse}")
            is_success_to_insert_wait_queue = False

            if startMatchResponse:
                is_success_to_insert_wait_queue = startMatchResponse.get("is_success")


            if is_success_to_insert_wait_queue:
                print("matching request success")
                self.__matchingWindow.updateMatchingBarWidth(0, rootWindow)
                rootWindow.after(3000, lambda: self.checkMatching(rootWindow))


            else:
                print("matching Window: Invalid or missing response data.")
                self.matchingCancel()

        except Exception as e:
            print(f"startMatch Error: {e}")
            self.matchingCancel()

    def matchingCancel(self):
        self.__isMatching = False
        self.__isRoomPrepared = False
        self.__matchingWindow.hideMatchingUI()
        self.__matchingWindow.destroy()

    def checkMatching(self, rootWindow):
        if self.__isMatching:
            from lobby_frame.controller.lobby_menu_frame_controller_impl import LobbyMenuFrameControllerImpl
            self.__matchingWindow.updateMatchingImage()

            isMatchingSuccessResponse = self.__matchingWindowRepository.checkMatching(
                CheckMatchingRequest(
                    self.__sessionRepository.get_session_info()
                )
            )
            currentStatus = isMatchingSuccessResponse.get("current_status")
            print(f"after request matching status: {currentStatus}")

            if currentStatus == "FAIL":
                self.__matchingWindow.changeWindowText("매칭 실패!")
                rootWindow.after(3000, lambda: self.matchingCancel())

            elif currentStatus == "SUCCESS":
                self.__matchingWindow.changeWindowText("매칭 성공!")
                self.__matchingWindow.hideMatchingUI()
                self.__waitForPrepareBattle()
                self.__saveRoomNumber()
                rootWindow.after(3000, lambda: LobbyMenuFrameControllerImpl.getInstance().switchFrameToBattleLobby(self.__matchingWindow))
                
            else:
                self.__matchingWindow.changeWindowText("매칭중입니다...")
                rootWindow.after(3000, lambda: self.checkMatching(rootWindow))

            #print("CheckMatching: Invalid response data")


    def getMatchingWindow(self):
        return self.__matchingWindow

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__matchingWindowRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__matchingWindowRepository.saveReceiveIpcChannel(receiveIpcChannel)