import tkinter as tk
import unittest
from PIL import ImageTk, Image




class TestCardShopFrame(unittest.TestCase):

    def createShopButtonUiFrame(self, root):

        def show_human_images():
            # 휴먼 이미지를 표시하는 동작을 구현합니다.
            pass

        def show_undead_images():
            # 언데드 이미지를 표시하는 동작을 구현합니다.
            pass

        def show_trent_images():
            # 트랜트 이미지를 표시하는 동작을 구현합니다.
            pass

        # 버튼 생성 및 배치
        human_button = tk.Button(root, text="휴먼", command=show_human_images)
        human_button.place(x=10, y=10)

        undead_button = tk.Button(root, text="언데드", command=show_undead_images)
        undead_button.place(x=10, y=50)

        trent_button = tk.Button(root, text="트랜트", command=show_trent_images)
        trent_button.place(x=10, y=90)


    def test_rock_paper_scissors(self):
        root = tk.Tk()
        root.geometry("200x980")
        root.configure(background="#151515")
        self.createShopButtonUiFrame(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
