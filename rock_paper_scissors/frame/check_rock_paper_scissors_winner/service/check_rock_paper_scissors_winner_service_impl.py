import tkinter
import time
import threading

from rock_paper_scissors.frame.check_rock_paper_scissors_winner.repository.check_rock_paper_scissors_winner_repository_impl import CheckRockPaperScissorsWinnerRepositoryImpl
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.service.request.check_rock_paper_scissors_winner_request import CheckRockPaperScissorsWinnerRequest
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.service.check_rock_paper_scissors_winner_service import CheckRockPaperScissorsWinnerService
from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl
from session.repository.session_repository_impl import SessionRepositoryImpl
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl


class CheckRockPaperScissorsWinnerServiceImpl(CheckRockPaperScissorsWinnerService):
    __instance = None
    __rockPaperScissorServiceImpl = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__checkRockPaperScissorsWinnerRepositoryImpl = CheckRockPaperScissorsWinnerRepositoryImpl.getInstance()
            cls.__instance.__sessionRepositoryImpl = SessionRepositoryImpl.getInstance()
            cls.__instance.__notifyReaderRepositoryImpl = NotifyReaderRepositoryImpl.getInstance()
            cls.__instance.__rockPaperScissorRepositoryImpl = RockPaperScissorsRepositoryImpl.getInstance()
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

        # for i in range(70):
        #     time.sleep(1)
        #     responseData = self.__checkRockPaperScissorsWinnerRepositoryImpl.requestCheckRockPaperScissorsWinner(
        #         CheckRockPaperScissorsWinnerRequest(self.__sessionRepositoryImpl.get_session_info()))
        #     print(f"responseData: {responseData}")
        #
        #     if responseData.get("am_i_first_turn") in ("WIN", "LOSE"):
        #         self.__checkRockPaperScissorsWinnerRepositoryImpl.setRPSWinner(responseData.get("am_i_first_turn"))
        #         self.check_RPS_label.configure(text="당신이 " + self.findWinner() + "입니다.")
        #         # self.__notifyReaderRepositoryImpl.set_is_your_turn_for_check_fake_process(self.setWinnerToNotify())
        #         checkRockPaperScissorsWinnerFrame.update()
        #         time.sleep(5)
        #         self.__rockPaperScissorRepositoryImpl.resetRPS()
        #         self.__rockPaperScissorRepositoryImpl.setcheckRPS(False)
        #         from rock_paper_scissors.service.rock_paper_scissors_service_impl import RockPaperScissorsServiceImpl
        #         self.__rockPaperScissorServiceImpl = RockPaperScissorsServiceImpl.getInstance()
        #         self.__rockPaperScissorServiceImpl.createRockPaperScissorsFrame(checkRockPaperScissorsWinnerFrame, switchFrameWithMenuName)
        #         switchFrameWithMenuName('battle-field-muligun')
        #         break
        #
        #     checkRockPaperScissorsWinnerFrame.update()

        return checkRockPaperScissorsWinnerFrame

    def check_RPSWinner(self, rootWindow, switchFrameWithMenuName):
        checkRockPaperScissorsWinnerFrame = self.__checkRockPaperScissorsWinnerRepositoryImpl.createCheckRockPaperScissorsWinnerFrame(
            rootWindow)
        count = 0
        if count < 70:
            responseData = self.__checkRockPaperScissorsWinnerRepositoryImpl.requestCheckRockPaperScissorsWinner(
                CheckRockPaperScissorsWinnerRequest(self.__sessionRepositoryImpl.get_session_info()))
            print(f"responseData: {responseData}")

            if responseData.get("am_i_first_turn") in ("WIN", "LOSE"):
                self.__checkRockPaperScissorsWinnerRepositoryImpl.setRPSWinner(responseData.get("am_i_first_turn"))
                self.check_RPS_label.configure(text="당신이 " + self.findWinner() + "입니다.")
                time.sleep(5)
                self.__rockPaperScissorRepositoryImpl.resetRPS()
                # self.__rockPaperScissorRepositoryImpl.setcheckRPS(False)
                # from rock_paper_scissors.service.rock_paper_scissors_service_impl import RockPaperScissorsServiceImpl
                # self.__rockPaperScissorServiceImpl = RockPaperScissorsServiceImpl.getInstance()
                switchFrameWithMenuName('battle-field-muligun')
                return

            checkRockPaperScissorsWinnerFrame.after(1000, self.check_RPSWinner, switchFrameWithMenuName, count + 1)

    def findWinner(self):
        RPSWinner_mapping = {
            "WIN": "선공",
            "LOSE": "후공"
        }
        RPSWinner = self.__checkRockPaperScissorsWinnerRepositoryImpl.getRPSWinner()
        print(f"RPSWinner: {RPSWinner}")
        RPSWinnerResult = RPSWinner_mapping.get(RPSWinner, "Unknown")
        return RPSWinnerResult

    # def setWinnerToNotify(self):
    #     RPSWinner_mapping = {
    #         "WIN": True,
    #         "LOSE": False
    #     }
    #     RPSWinner = self.__checkRockPaperScissorsWinnerRepositoryImpl.getRPSWinner()
    #     print(f"RPSWinner: {RPSWinner}")
    #     RPSWinnerResult = RPSWinner_mapping.get(RPSWinner, "Unknown")
    #     return RPSWinnerResult



    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("CheckRockPaperScissorsWinnerServiceImpl: injectTransmitIpcChannel()")
        self.__checkRockPaperScissorsWinnerRepositoryImpl.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("CheckRockPaperScissorsWinnerServiceImpl: injectReceiveIpcChannel()")
        self.__checkRockPaperScissorsWinnerRepositoryImpl.saveReceiveIpcChannel(receiveIpcChannel)
