import tkinter
import unittest
from PIL import ImageTk, Image

from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl
from rock_paper_scissors.service.request.rock_paper_scissors_request import RockPaperScissorsRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class TestRockPaperScissors(unittest.TestCase):

    def createRockPaperScissorsUiFrame(self, rootWindow):
        # ljs/test_notify_reader/test_motify_opponent_unit_spawn참고
        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()

    def test_rock_paper_scissors(self):
        root = tkinter.Tk()
        root.geometry("1920x1080")
        root.configure(background="#151515")
        self.createRockPaperScissorsUiFrame(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()