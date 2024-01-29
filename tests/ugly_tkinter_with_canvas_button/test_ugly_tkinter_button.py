import tkinter as tk
import unittest


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.add_button = tk.Button(root, text="Add Shapes", command=self.add_shapes)
        self.add_button.pack(pady=10)

    def add_shapes(self):
        x, y = 200, 200  # 원의 중심 좌표
        radius = 50  # 원의 반지름
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="black")

        x_rect, y_rect = 100, 100  # 사각형의 좌상단 좌표
        width, height = 80, 120  # 사각형의 너비와 높이
        self.canvas.create_rectangle(x_rect, y_rect, x_rect + width, y_rect + height, outline="black", fill="black", stipple="gray50")

class TestUglyTkinterWithCanvasButton(unittest.TestCase):
    def test_tkinter_with_canvas_button(self):
        root = tk.Tk()
        app = DrawingApp(root)
        root.mainloop()


if __name__ == '__main__':
    unittest.main()
