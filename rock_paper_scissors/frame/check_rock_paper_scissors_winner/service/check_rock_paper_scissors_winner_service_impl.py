import tkinter
import time
import threading

from rock_paper_scissors.frame.check_rock_paper_scissors_winner.repository.check_rock_paper_scissors_winner_repository_impl import CheckRockPaperScissorsWinnerRepositoryImpl
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.service.request.check_rock_paper_scissors_winner_request import CheckRockPaperScissorsWinnerRequest
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.service.check_rock_paper_scissors_winner_service import CheckRockPaperScissorsWinnerService
from session.repository.session_repository_impl import SessionRepositoryImpl


class CheckRockPaperScissorsWinnerServiceImpl(CheckRockPaperScissorsWinnerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__checkRockPaperScissorsWinnerRepositoryImpl = CheckRockPaperScissorsWinnerRepositoryImpl.getInstance()
            cls.__instance.__sessionRepositoryImpl = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def createCheckRockPaperScissorsWinnerUiFrame(self, rootWindow, switchFrameWithMenuName):
        checkRockPaperScissorsWinnerFrame = self.__checkRockPaperScissorsWinnerRepositoryImpl.createCheckRockPaperScissorsWinnerFrame(rootWindow)

        frame = tkinter.Frame(checkRockPaperScissorsWinnerFrame, bg="#D8D8D8")
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=0.5)

        label_text = "상대방의 선택을 기다리는중"
        self.check_RPS_label = tkinter.Label(frame, text=label_text, font=("Helvetica", 32), fg="black",
                                        anchor="center", justify="center", bg="#D8D8D8")

        self.check_RPS_label.place(relx=0.5, rely=0.5, anchor="center", bordermode="outside", relwidth=0.5, relheight=0.5)

        checkRockPaperScissorsWinnerFrame.pack()

        for i in range(60):
            responseData = self.__checkRockPaperScissorsWinnerRepositoryImpl.requestCheckRockPaperScissorsWinner(
                CheckRockPaperScissorsWinnerRequest(self.__sessionRepositoryImpl.get_session_info()))
            print(f"responseData: {responseData}")
            time.sleep(1)

            if responseData.get("am_i_first_turn") in ("WIN", "LOSE"):
                self.__checkRockPaperScissorsWinnerRepositoryImpl.setRPSWinner(responseData.get("am_i_first_turn"))
                self.check_RPS_label.configure(text="당신이 " + self.findWinner() + "입니다.")
                time.sleep(3)
                break

        return checkRockPaperScissorsWinnerFrame

    def findWinner(self):
        RPSWinner_mapping = {
            "WIN": "선공",
            "LOSE": "후공"
        }
        RPSWinner = self.__checkRockPaperScissorsWinnerRepositoryImpl.getRPSWinner()
        print(f"RPSWinner: {RPSWinner}")
        RPSWinnerResult = RPSWinner_mapping.get(RPSWinner, "Unknown")
        return RPSWinnerResult



    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("CheckRockPaperScissorsWinnerServiceImpl: injectTransmitIpcChannel()")
        self.__checkRockPaperScissorsWinnerRepositoryImpl.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("CheckRockPaperScissorsWinnerServiceImpl: injectReceiveIpcChannel()")
        self.__checkRockPaperScissorsWinnerRepositoryImpl.saveReceiveIpcChannel(receiveIpcChannel)
