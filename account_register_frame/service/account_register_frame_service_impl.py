from tkinter import ttk

from account_register_frame.repository.account_register_frame_repository_impl import AccountRegisterFrameRepositoryImpl
from account_register_frame.service.account_register_frame_service import AccountRegisterFrameService
from account_register_frame.service.request.account_register_request import AccountRegisterRequest


class AccountRegisterFrameServiceImpl(AccountRegisterFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountRegisterFrameRepository = AccountRegisterFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createAccountRegisterUiFrame(self, rootWindow):
        accountRegisterFrame = self.__accountRegisterFrameRepository.createAccountRegisterFrame(rootWindow)

        style = ttk.Style()
        style.configure("TFrame", background="#444444")
        style.configure("TLabel", background="#444444", foreground="#ffffff", font=("Arial", 12))
        style.configure("TButton", background="#2C3E50", foreground="#ffffff", font=("Arial", 12), padding=(10, 5))

        label_username = ttk.Label(accountRegisterFrame, text="아이디:", style="TLabel")
        label_password = ttk.Label(accountRegisterFrame, text="비밀번호:", style="TLabel")
        entry_username = ttk.Entry(accountRegisterFrame, font=("Arial", 12))
        entry_password = ttk.Entry(accountRegisterFrame, show="*", font=("Arial", 12))

        # link_signup = ttk.Label(accountRegisterFrame, text="회원 가입", cursor="hand2", font=("Arial", 10, "underline"))
        # link_signup.bind("<Button-1>", self.__accountRegisterFrameRepository.requestLogin(entry_username.get(), entry_password.get()))
        link_signup = ttk.Label(accountRegisterFrame, text="회원 가입", cursor="hand2", font=("Arial", 10, "underline"))

        def on_signup_click(event):
            self.__accountRegisterFrameRepository.requestLogin(
                AccountRegisterRequest(entry_username.get(), entry_password.get()))

        link_signup.bind("<Button-1>", on_signup_click)

        label_username.place(relx=0.44, rely=0.4, anchor="center")
        entry_username.place(relx=0.56, rely=0.4, anchor="center")

        label_password.place(relx=0.44, rely=0.5, anchor="center")
        entry_password.place(relx=0.56, rely=0.5, anchor="center")

        link_signup.place(relx=0.5, rely=0.6, anchor="center")

        return accountRegisterFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("AccountRegisterFrameService: injectTransmitIpcChannel()")
        self.__accountRegisterFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)


