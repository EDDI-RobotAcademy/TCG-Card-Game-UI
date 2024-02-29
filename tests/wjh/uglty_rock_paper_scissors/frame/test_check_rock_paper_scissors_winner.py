import tkinter
import time
import unittest
from PIL import ImageTk, Image

from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl
from rock_paper_scissors.service.request.check_rock_paper_scissors_winner_request import CheckRockPaperScissorsWinnerRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class TestRockPaperScissors(unittest.TestCase):

    def createCheckRockPaperScissorsWinnerUiFrame(self, rootWindow):
        self.__rockPaperScissorsRepositoryImpl = RockPaperScissorsRepositoryImpl.getInstance()
        self.__sessionRepositoryImpl = SessionRepositoryImpl.getInstance()

        frame = tkinter.Frame(rootWindow, bg="#D8D8D8")
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=0.5)

        label_text = "상대방의 선택을 기다리는중"
        check_RPS_label = tkinter.Label(frame, text=label_text, font=("Helvetica", 32), fg="black",
                                  anchor="center", justify="center", bg="#D8D8D8")

        check_RPS_label.place(relx=0.5, rely=0.5, anchor="center", bordermode="outside", relwidth=0.5, relheight=0.5)
        for i in range(60):
            responseData = self.__rockPaperScissorsRepositoryImpl.requestCheckRockPaperScissorsWinner(
                CheckRockPaperScissorsWinnerRequest(self.__sessionRepositoryImpl.get_session_info()))
            time.sleep(1)
            if responseData is not None:
                check_RPS_label.configure(text="당신은 "+responseData+"입니다.")
                time.sleep(3)





    def test_check_rock_paper_scissors_winner(self):
        root = tkinter.Tk()
        root.geometry("1920x1080")
        root.configure(background="#151515")
        self.createCheckRockPaperScissorsWinnerUiFrame(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
