import tkinter as tk
import unittest


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}-0-0")

        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="green")
        self.canvas.pack()

        # 버튼을 누를 때마다 상태가 토글되도록 하는 변수
        self.toggle_state = False

        self.toggle_button = tk.Button(root, text="Toggle Shapes", command=self.toggle_shapes)
        self.toggle_button.place(x=10, y=10)

        # 현재 추가된 모든 도형의 ID를 저장하는 리스트
        self.shape_ids = []

    def toggle_shapes(self):
        # 토글 상태에 따라 add_shapes 또는 clear_shapes 호출
        if self.toggle_state:
            self.clear_shapes()
        else:
            self.add_shapes()
        # 토글 상태 변경
        self.toggle_state = not self.toggle_state

    def add_shapes(self):
        # 투명한 검정색 사각형
        rect_id1 = self.canvas.create_rectangle(0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight(),
                                               outline="black", fill="black", stipple="gray50")
        self.shape_ids.append(rect_id1)

        # 노란색 사각형
        x_rect, y_rect = 200, 200  # 사각형의 좌상단 좌표
        width, height = 100, 150  # 사각형의 너비와 높이
        rect_id2 = self.canvas.create_rectangle(x_rect, y_rect, x_rect + width, y_rect + height,
                                               outline="black", fill="yellow")
        self.shape_ids.append(rect_id2)

    def clear_shapes(self):
        # 현재 추가된 모든 도형 삭제
        for shape_id in self.shape_ids:
            self.canvas.delete(shape_id)
        # 모든 도형 ID 초기화
        self.shape_ids = []


class TestUglyTkinterWithCanvasButton(unittest.TestCase):
    def test_tkinter_with_canvas_button(self):
        root = tk.Tk()
        app = DrawingApp(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
