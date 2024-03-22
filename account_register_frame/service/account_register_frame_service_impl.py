from tkinter import ttk
import tkinter
from PIL import ImageTk, Image

from account_register_frame.repository.account_register_frame_repository_impl import AccountRegisterFrameRepositoryImpl
from account_register_frame.service.account_register_frame_service import AccountRegisterFrameService
from account_register_frame.service.request.account_register_request import AccountRegisterRequest
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl


class AccountRegisterFrameServiceImpl(AccountRegisterFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountRegisterFrameRepository = AccountRegisterFrameRepositoryImpl.getInstance()
            cls.__instance.__musicPlayerRepository = MusicPlayerRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createAccountRegisterUiFrame(self, rootWindow, switchFrameWithMenuName):
        accountRegisterFrame = self.__accountRegisterFrameRepository.createAccountRegisterFrame(rootWindow)

        style = ttk.Style()
        style.configure("TFrame", background="#444444")
        style.configure("TLabel", background="#444444", foreground="#ffffff", font=("Arial", 12))
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

        # label_username = ttk.Label(accountRegisterFrame, text="아이디:", style="TLabel")
        # label_password = ttk.Label(accountRegisterFrame, text="비밀번호:", style="TLabel")
        entry_username = ttk.Entry(accountRegisterFrame, font=("Arial", 20))
        entry_username.insert(0, "ID")
        entry_username.bind("<FocusIn>", on_entry_click_user_name)

        entry_password = ttk.Entry(accountRegisterFrame, font=("Arial", 20))
        entry_password.insert(0, "PASSWORD")
        entry_password.bind("<FocusIn>", on_entry_click_password)

        # 회원 가입 버튼
        self.button_sign_up_origin = Image.open("local_storage/sign_up_screen_image/sign_up_screen_button.png")
        sign_up_button = self.button_sign_up_origin.resize((271, 67))
        self.button_sign_up = ImageTk.PhotoImage(sign_up_button)

        # link_signup = ttk.Label(accountRegisterFrame, text="회원 가입", cursor="hand2", font=("Arial", 10, "underline"))
        # link_signup.bind("<Button-1>", self.__accountRegisterFrameRepository.requestLogin(entry_username.get(), entry_password.get()))
        # link_signup = ttk.Label(accountRegisterFrame,
        #                         text="회원 가입", cursor="hand2", font=("Arial", 10, "underline"))

        signup_button = tkinter.Button(accountRegisterFrame,
                                       image=self.button_sign_up,
                                       bd=0, highlightthickness=0,
                                       width=271, height=67)

        def on_signup_click(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')
            try:
                responseData = self.__accountRegisterFrameRepository.requestRegister(
                    AccountRegisterRequest(entry_username.get(), entry_password.get()))

                print(f"responseData: {responseData}")

                if responseData and responseData.get("is_success") is True:
                    switchFrameWithMenuName("login-menu")
                else:
                    print("Invalid or missing response data.")
            except Exception as e:
                print(f"An error occurred: {e}")

        signup_button.bind("<Button-1>", on_signup_click)

        # label_username.place(relx=0.44, rely=0.4, anchor="center")
        entry_username.place(relx=0.5, rely=0.497, width=457, height=68, anchor="center")

        # label_password.place(relx=0.44, rely=0.5, anchor="center")
        entry_password.place(relx=0.5, rely=0.605, width=457, height=68, anchor="center")

        signup_button.place(relx=0.5, rely=0.784, anchor="center")

        def play_mouse_on_button_sound(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('mouse_on_button')

        signup_button.bind('<Enter>', play_mouse_on_button_sound)

        return accountRegisterFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("AccountRegisterFrameService: injectTransmitIpcChannel()")
        self.__accountRegisterFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("AccountRegisterFrameService: injectTransmitIpcChannel()")
        self.__accountRegisterFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)


