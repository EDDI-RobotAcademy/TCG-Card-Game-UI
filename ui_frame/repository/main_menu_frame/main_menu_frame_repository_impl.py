import tkinter

from ui_frame.entity.main_menu_frame import MainMenuFrame
from ui_frame.repository.main_menu_frame.main_menu_frame_repository import MainMenuFrameRepository


class MainMenuFrameRepositoryImpl(MainMenuFrameRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMainMenuFrame(self, rootWindow):
        print("MainMenuFrameRepositoryImpl: createMainMenuFrame()")
        mainMenuFrame = MainMenuFrame(rootWindow)

        label_text = "EDDI TCG Card Battle"
        label = tkinter.Label(mainMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.5, anchor="center", bordermode="outside")  # 가운데 정렬

        start_button = tkinter.Button(mainMenuFrame, text="시작", bg="#2E7D32", fg="white", width=36, height=2)
        start_button.place(relx=0.5, rely=0.65, anchor="center")

        exit_button = tkinter.Button(mainMenuFrame, text="종료", bg="#C62828", fg="white", width=36, height=2)
        exit_button.place(relx=0.5, rely=0.75, anchor="center")
        mainMenuFrame.pack(expand=True, fill="both")

        return mainMenuFrame
