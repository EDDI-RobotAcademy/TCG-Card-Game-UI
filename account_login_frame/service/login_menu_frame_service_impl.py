from tkinter import ttk

from account_login_frame.repository.login_menu_frame_repository_impl import LoginMenuFrameRepositoryImpl
from account_login_frame.service.login_menu_frame_service import LoginMenuFrameService


class LoginMenuFrameServiceImpl(LoginMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__loginMenuFrameRepository = LoginMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createLoginUiFrame(self, rootWindow, switchFrameWithMenuName):
        loginMenuFrame = self.__loginMenuFrameRepository.createLoginMenuFrame(rootWindow)

        style = ttk.Style()
        style.configure("TFrame", background="#444444")
        style.configure("TLabel", background="#444444", foreground="#ffffff", font=("Arial", 12))
        style.configure("TButton", background="#2C3E50", foreground="#ffffff", font=("Arial", 12), padding=(10, 5))

        label_username = ttk.Label(loginMenuFrame, text="아이디:", style="TLabel")
        label_password = ttk.Label(loginMenuFrame, text="비밀번호:", style="TLabel")
        entry_username = ttk.Entry(loginMenuFrame, font=("Arial", 12))
        entry_password = ttk.Entry(loginMenuFrame, show="*", font=("Arial", 12))

        # button_login = ttk.Button(loginMenuFrame, text="로그인", command=loginMenuFrame.login, style="TButton")
        button_login = ttk.Button(loginMenuFrame, text="로그인", style="TButton")
        link_signup = ttk.Label(loginMenuFrame, text="회원 가입", cursor="hand2", font=("Arial", 10, "underline"))
        link_signup.bind("<Button-1>", lambda event: switchFrameWithMenuName("account-register"))

        label_username.place(relx=0.44, rely=0.4, anchor="center")
        entry_username.place(relx=0.56, rely=0.4, anchor="center")

        label_password.place(relx=0.44, rely=0.5, anchor="center")
        entry_password.place(relx=0.56, rely=0.5, anchor="center")

        button_login.place(relx=0.5, rely=0.6, anchor="center")
        link_signup.place(relx=0.5, rely=0.7, anchor="center")

        return loginMenuFrame
