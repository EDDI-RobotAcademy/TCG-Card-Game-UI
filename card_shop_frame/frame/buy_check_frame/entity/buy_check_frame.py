import tkinter


class BuyCheckFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(width=500, height=700)

        self.image_label = tkinter.Label(self, bd=0, highlightthickness=0)
        self.image_label.pack(fill="both", expand=True)

    def set_image(self, image):
        # 이미지 설정
        self.image_label.config(image=image)
        self.image_label.image = image
