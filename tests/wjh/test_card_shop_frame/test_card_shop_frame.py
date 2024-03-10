import tkinter as tk
import unittest
from PIL import ImageTk, Image




class TestCardShopFrame(unittest.TestCase):

    def createCardShopUiFrame(self, root):
        def show_human_images():
            # 휴먼 이미지를 표시하는 동작을 구현합니다.
            pass

        def show_undead_images():
            # 언데드 이미지를 표시하는 동작을 구현합니다.
            pass

        def show_trent_images():
            # 트랜트 이미지를 표시하는 동작을 구현합니다.
            pass

        # 각 프레임을 생성합니다.
        top_frame = tk.Frame(root, width=1920, height=50, bg="red")  # 상단 프레임
        middle_frame = tk.Frame(root, width=200, height=1030, bg="green")  # 왼쪽 프레임
        bottom_frame = tk.Frame(root, width=1720, height=1030, bg="blue")  # 오른쪽 프레임

        # 프레임을 배치합니다.
        top_frame.place(x=0, y=0)
        middle_frame.place(x=0, y=70)
        bottom_frame.place(x=200, y=70)

        # 상점 레이블 생성 및 배치
        shop_label = tk.Label(top_frame, text="상점", font=("Helvetica", 16))
        shop_label.place(x=10, y=10)

        # 버튼 생성 및 배치
        human_button = tk.Button(middle_frame, text="휴먼", command=show_human_images)
        human_button.place(x=10, y=10)

        undead_button = tk.Button(middle_frame, text="언데드", command=show_undead_images)
        undead_button.place(x=10, y=50)

        trent_button = tk.Button(middle_frame, text="트랜트", command=show_trent_images)
        trent_button.place(x=10, y=90)

        # 이미지 표시 영역 생성 (여기서는 더미 텍스트로 대체)
        image_display = tk.Label(bottom_frame, text="이미지가 여기에 나타납니다.", font=("Helvetica", 12))
        image_display.place(x=10, y=10)


    def test_rock_paper_scissors(self):
        root = tk.Tk()
        root.geometry("1920x1080")
        root.configure(background="#151515")
        self.createCardShopUiFrame(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
