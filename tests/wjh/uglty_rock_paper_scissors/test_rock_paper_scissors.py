import tkinter
import unittest
from PIL import ImageTk, Image

from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl
from rock_paper_scissors_button.paper_button import PaperButton


class TestRockPaperScissors(unittest.TestCase):

    def createRockPaperScissorsUiFrame(self, rootWindow):
        self.__rockPaperScissorsRepositoryImpl = RockPaperScissorsRepositoryImpl.getInstance()

        def final_decision_button_click(target_rps):
            print(target_rps)
            #self.__rockPaperScissorsRepositoryImpl.setRPS(target_rps)

        def on_paper_image_click(event):
            self.__rockPaperScissorsRepositoryImpl.setRPS("보")
            RPS_label.config(text=self.__rockPaperScissorsRepositoryImpl.getRPS())

        image_path = "/home/eddi/proj/TCG-Card-Game-UI/local_storage/rock_paper_scissors_image/paper.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 250), Image.LANCZOS)
        self.__paper_image = ImageTk.PhotoImage(resized_image)

        paper_label = tkinter.Label(rootWindow, image=self.__paper_image)
        paper_label.place(x=400, y=200)
        paper_label.bind("<Button-1>", on_paper_image_click)

        def on_scissors_image_click(event):
            self.__rockPaperScissorsRepositoryImpl.setRPS("가위")
            RPS_label.config(text=self.__rockPaperScissorsRepositoryImpl.getRPS())

        image_path = "/home/eddi/proj/TCG-Card-Game-UI/local_storage/rock_paper_scissors_image/scissors.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 250), Image.LANCZOS)
        self.__scissors_image = ImageTk.PhotoImage(resized_image)

        scissors_label = tkinter.Label(rootWindow, image=self.__scissors_image)
        scissors_label.place(x=700, y=200)
        scissors_label.bind("<Button-1>", on_scissors_image_click)

        def on_rock_image_click(event):
            self.__rockPaperScissorsRepositoryImpl.setRPS("바위")
            RPS_label.config(text=self.__rockPaperScissorsRepositoryImpl.getRPS())

        image_path = "/home/eddi/proj/TCG-Card-Game-UI/local_storage/rock_paper_scissors_image/rock.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 250), Image.LANCZOS)
        self.__rock_image = ImageTk.PhotoImage(resized_image)

        rock_label = tkinter.Label(rootWindow, image=self.__rock_image)
        rock_label.place(x=1000, y=200)
        rock_label.bind("<Button-1>", on_rock_image_click)


        label_text = self.__rockPaperScissorsRepositoryImpl.getRPS()
        RPS_label = tkinter.Label(rootWindow, text=label_text, font=("Helvetica", 32), fg="black",
                              anchor="center", justify="center")

        RPS_label.place(relx=0.5, rely=0.8, anchor="center", bordermode="outside")  # 가운데 정렬



        self.final_decision_button = tkinter.Button(rootWindow, text="선택 완료", bg="#2E2BE2", fg="white",
                                             command=lambda: final_decision_button_click(self.__rockPaperScissorsRepositoryImpl.getRPS()),
                                             width=24, height=2)
        self.final_decision_button.place(relx=0.5, rely=0.9, anchor="center")


    def test_rock_paper_scissors(self):
        root = tkinter.Tk()
        root.geometry("1920x800")
        root.configure(background="#E1F5A9")
        self.createRockPaperScissorsUiFrame(root)
        root.mainloop()


if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("1920x800")
    unittest.main()
