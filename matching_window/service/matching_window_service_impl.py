import tkinter

from battle_lobby_frame.controller.battle_lobby_frame_controller_impl import BattleLobbyFrameControllerImpl
from matching_window.repository.matching_window_repository_impl import MatchingWindowRepositoryImpl
from matching_window.service.matching_window_service import MatchingWindowService
from matching_window.service.request.cancel_matching_request import CancelMatchingRequest
from matching_window.service.request.check_matching_request import CheckMatchingRequest
from matching_window.service.request.start_matching_request import StartMatchingRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from utility.image_generator import ImageGenerator


imageWidth = 256
imageHeight = 256

class MatchingWindowServiceImpl(MatchingWindowService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__matchingWindowRepository = MatchingWindowRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__battleLobbyFrameController = BattleLobbyFrameControllerImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

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
                self.__matchingWindow.destroy()

        self.__matchingWindow.getCancelMatchingButton.bind("<Button-1>", onClickCancelMatchingButton)
        rootWindow.update()

    def startMatching(self, rootWindow):
        try:
            afterBattleMatchResponse = self.__matchingWindowRepository.requestMatching(
                StartMatchingRequest(
                    self.__sessionRepository.get_session_info()
                )
            )

            is_success_to_insert_wait_queue = False

            if afterBattleMatchResponse:
                is_success_to_insert_wait_queue = afterBattleMatchResponse.get("is_success")

            if is_success_to_insert_wait_queue:
                self.__matchingWindow.updateMatchingBarWidth(0, rootWindow)
                return rootWindow.after(3000, lambda : self.checkMatching(rootWindow))

            else:
                print("Invalid or missing response data.")


        except Exception as e:
            print(f"startMatch Error: {e}")

        self.__matchingWindow.hideMatchingUI()
        return False

    def checkMatching(self, rootWindow):
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
            rootWindow.after(3000, lambda: self.__matchingWindow.destroy)
            return False

        if currentStatus == "WAIT":
            self.__matchingWindow.changeWindowText("매칭중입니다...")
            rootWindow.after(3000, lambda: self.checkMatching(rootWindow))

        # else:
        if currentStatus == "SUCCESS":
            self.__matchingWindow.changeWindowText("매칭 성공!")
            self.__matchingWindow.hideMatchingUI()
            return True


    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__matchingWindowRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__matchingWindowRepository.saveReceiveIpcChannel(receiveIpcChannel)