from tkinter import ttk

from account_register_frame.entity.account_register_frame import AccountRegisterFrame
from account_register_frame.repository.account_register_frame_repository import AccountRegisterFrameRepository


class AccountRegisterFrameRepositoryImpl(AccountRegisterFrameRepository):
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

    def createAccountRegisterFrame(self, rootWindow):
        print("AccountRegisterFrameRepositoryImpl: createAccountRegisterFrame()")
        accountRegisterFrame = AccountRegisterFrame(rootWindow)

        style = ttk.Style()
        style.configure("TFrame", background="#444444")
        style.configure("TLabel", background="#444444", foreground="#ffffff", font=("Arial", 12))
        style.configure("TButton", background="#2C3E50", foreground="#ffffff", font=("Arial", 12), padding=(10, 5))

        label_username = ttk.Label(accountRegisterFrame, text="아이디:", style="TLabel")
        label_password = ttk.Label(accountRegisterFrame, text="비밀번호:", style="TLabel")
        entry_username = ttk.Entry(accountRegisterFrame, font=("Arial", 12))
        entry_password = ttk.Entry(accountRegisterFrame, show="*", font=("Arial", 12))

        button_login = ttk.Button(accountRegisterFrame, text="로그인", style="TButton")
        link_signup = ttk.Label(accountRegisterFrame, text="회원 가입", cursor="hand2", font=("Arial", 10, "underline"))
        link_signup.bind("<Button-1>")

        label_username.place(relx=0.44, rely=0.4, anchor="center")
        entry_username.place(relx=0.56, rely=0.4, anchor="center")

        label_password.place(relx=0.44, rely=0.5, anchor="center")
        entry_password.place(relx=0.56, rely=0.5, anchor="center")

        button_login.place(relx=0.5, rely=0.6, anchor="center")
        link_signup.place(relx=0.5, rely=0.7, anchor="center")

        return accountRegisterFrame

