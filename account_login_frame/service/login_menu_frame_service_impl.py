from tkinter import ttk
import tkinter
from PIL import ImageTk, Image

from account_login_frame.repository.login_menu_frame_repository_impl import LoginMenuFrameRepositoryImpl
from account_login_frame.service.login_menu_frame_service import LoginMenuFrameService
from account_login_frame.service.request.account_login_request import AccountLoginRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class LoginMenuFrameServiceImpl(LoginMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__loginMenuFrameRepository = LoginMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
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
        style.configure("TLabel", background="#444444", foreground="#ffffff", font=("Arial", 13))
        style.configure("TButton", background="#2C3E50", foreground="#ffffff", font=("Arial", 12), padding=(10, 5))
        style.configure("TEntry", foreground="gray")

        def on_entry_click_user_name(event):
            if entry_username.get() == "ID":
                entry_username.delete(0, "end")
                style.configure("TEntry", foreground="black")

        def on_entry_click_password(evnet):
            if entry_password.get() == "PASSWORD":
                entry_password.delete(0, "end")
                style.configure("TEntry", foreground="black")
                entry_password["show"] = "*"


        # label_username = ttk.Label(loginMenuFrame, text="아이디:", style="TLabel")
        # label_password = ttk.Label(loginMenuFrame, text="비밀번호:", style="TLabel")
        entry_username = ttk.Entry(loginMenuFrame, font=("Arial", 20))
        entry_username.insert(0, "ID")
        entry_username.bind("<FocusIn>", on_entry_click_user_name)

        entry_password = ttk.Entry(loginMenuFrame, font=("Arial", 20))
        entry_password.insert(0, "PASSWORD")
        entry_password.bind("<FocusIn>", on_entry_click_password)

        # button_login = ttk.Button(loginMenuFrame, text="로그인", command=loginMenuFrame.login, style="TButton")

        # 로그인 버튼 resize
        self.button_login_origin = Image.open("local_storage/login_screen_image/login_screen_button.png")
        login_button = self.button_login_origin.resize((271, 67))
        self.button_login = ImageTk.PhotoImage(login_button)

        button_login = tkinter.Button(loginMenuFrame,
                                      image=self.button_login,
                                      bd=0, highlightthickness=0,
                                      width=271, height=67)
        # button_login.bind("<Button-1>", lambda event: switchFrameWithMenuName("lobby-menu"))


        def on_signin_click(event):
            try:
                responseData = self.__loginMenuFrameRepository.requestLogin(
                    AccountLoginRequest(entry_username.get(), entry_password.get()))

                print(f"responseData: {responseData}")

                # TODO: Session 처리 필요함
                if responseData:
                    redis_token = responseData.get("redis_token")

                    if redis_token is not None and isinstance(redis_token, str) and redis_token != "":
                        print(f"Valid redis_token received: {redis_token}")

                        self.__sessionRepository.writeRedisTokenSessionInfoToFile(redis_token)

                        switchFrameWithMenuName("lobby-menu")
                    else:
                        print("Invalid or missing redis_token in response data.")
                else:
                    print("Invalid or missing response data.")
            except Exception as e:
                print(f"An error occurred: {e}")

        # link_signup.bind("<Button-1>", on_signup_click)
        button_login.bind("<Button-1>", on_signin_click)

        link_signup = ttk.Label(loginMenuFrame, text="회원 가입", cursor="hand2", font=("Arial", 13, "underline"))
        link_signup.bind("<Button-1>", lambda event: switchFrameWithMenuName("account-register"))

        # label_username.place(relx=0.44, rely=0.4, anchor="center")
        entry_username.place(relx=0.5, rely=0.497, width=457, height=68, anchor="center")

        # label_password.place(relx=0.44, rely=0.5, anchor="center")
        entry_password.place(relx=0.5, rely=0.605, width=457, height=68, anchor="center")

        button_login.place(relx=0.5, rely=0.784, anchor="center")
        link_signup.place(relx=0.5, rely=0.85, anchor="center")

        # def on_enter():
        #     on_signin_click(event='<Return>')
        #
        # loginMenuFrame.bind('<Return>', lambda event: on_enter)
        entry_password.bind("<Return>", on_signin_click)

        return loginMenuFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("LoginMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__loginMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("LoginMenuFrameServiceImpl: injectReceiveIpcChannel()")
        self.__loginMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)




