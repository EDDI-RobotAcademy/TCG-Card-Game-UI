class MyDeckRegisterRectangle:
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas
        self.width = 800
        self.height = 500

    def create_rectangle(self, main_frame_width, main_frame_height):
        window_width = self.canvas.winfo_reqwidth()
        window_height = self.canvas.winfo_reqheight()

        # 계산을 통해 도형을 화면 정 가운데에 띄우기
        x1 = (main_frame_width - self.width) // 2
        y1 = (main_frame_height - self.height) // 2
        x2 = x1 + self.width
        y2 = y1 + self.height

        my_deck_register_rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill='#966F33')

        return my_deck_register_rectangle