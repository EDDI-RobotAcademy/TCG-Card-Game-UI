import tkinter
from PIL import ImageTk, Image

class AccountRegisterFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg="#000000")
        self.create_widgets()

    def create_widgets(self):
        self.label = tkinter.Label(self)
        self.label.place(anchor="nw")

        self.load_image()
        self.display_image()

        self.prev_width = self.master.winfo_width()
        self.prev_height = self.master.winfo_height()

        self.bind_configure_event()

    def load_image(self):
        # 이미지 로드 및 Tkinter PhotoImage로 변환
        self.original_image = Image.open("local_storage/sign_up_screen_image/sign_up_screen.png")

    def display_image(self):
        # 이미지를 현재 창 크기에 맞게 리사이즈하고 Label에 표시
        resized_img = self.original_image.resize((self.master.winfo_width(), self.master.winfo_height()),
                                                 Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_img)
        self.label.config(image=self.image)

    def resize_image(self, event):
        # 창 크기 변경 이벤트에 따라 이미지 리사이즈 및 표시
        new_width = event.width
        new_height = event.height

        if new_width != self.prev_width or new_height != self.prev_height:
            # 이전 크기 갱신
            self.prev_width = new_width
            self.prev_height = new_height
            self.display_image()

    def on_configure(self, event):
        # 창 크기 변경 이벤트 처리
        self.display_image()

    def bind_configure_event(self):
        self.bind("<Configure>", self.on_configure)
