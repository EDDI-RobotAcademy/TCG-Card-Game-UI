import tkinter
from PIL import ImageTk, Image
from colorama import Fore, Style
from screeninfo import get_monitors

from main_frame.repository.main_menu_frame_repository_impl import MainMenuFrameRepositoryImpl
from main_frame.service.main_menu_frame_service import MainMenuFrameService
from main_frame.service.request.program_exit_request import ProgramExitRequest
from music_player.repository.music_player_repository_impl import MusicPlayerRepositoryImpl
from opengl_dummy_frame.repository.opengl_dummy_frame_repository import OpenGLDummyFrameRepository
from session.service.session_service_impl import SessionServiceImpl


class MainMenuFrameServiceImpl(MainMenuFrameService):
    __instance = None

    title_bar_height = None

    opengl_dummy_frame_repository = OpenGLDummyFrameRepository.getInstance()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__mainMenuFrameRepository = MainMenuFrameRepositoryImpl.getInstance()

            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
            cls.__instance.__musicPlayerRepository = MusicPlayerRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    # def check_full_screen_size(self):
    #     dummy_frame = self.opengl_dummy_frame_repository.get_dummy_frame()
    #     width = dummy_frame.get_real_width()
    #     height = dummy_frame.get_real_height()
    #
    #     print(f"main-menu frame width: {width}, height: {height}")

    def createMainUiFrame(self, rootWindow, switchFrameWithMenuName):
        # self.check_full_screen_size()
        mainMenuFrame = self.__mainMenuFrameRepository.createMainMenuFrame(rootWindow)
        # title_bar_height = mainMenuFrame.winfo_rooty() - mainMenuFrame.winfo_y()
        # print(f"{Fore.RED}title_bar_height: {title_bar_height}{Style.RESET_ALL}")
        # outer_window_height = mainMenuFrame.winfo_height() + title_bar_height
        # print(f"{Fore.RED}outer_window_height: {outer_window_height}{Style.RESET_ALL}")

        # label_text = "EDDI TCG Card Battle"
        # label = tkinter.Label(mainMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
        #                       anchor="center", justify="center", pady=50)
        #
        # label.place(relx=0.5, rely=0.5, anchor="center", bordermode="outside")  # 가운데 정렬

        # start_button = tkinter.Button(mainMenuFrame, text="시작", bg="#2E7D32", fg="white",
        #                               command=lambda: switchFrameWithMenuName("login-menu"), width=36, height=2)


        self.button_start_origin = Image.open("local_storage/start_screen_image/start_button.png")
        button_start = self.button_start_origin.resize((264, 67))
        self.start_login = ImageTk.PhotoImage(button_start)

        self.button_exit_origin = Image.open("local_storage/start_screen_image/exit_button.png")
        button_exit = self.button_exit_origin.resize((264, 67))
        self.button_exit = ImageTk.PhotoImage(button_exit)

        start_button = tkinter.Button(mainMenuFrame,
                                      image=self.start_login,
                                      bd=0, highlightthickness=0,
                                      width=264, height=67)

        def on_session_login_click(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')
            try:
                if self.__sessionService.getSessionInfo() is not None:
                    responseData = self.__sessionService.requestLoginWithSession()
                    if responseData:
                        redis_token = responseData.get("redis_token")

                        if redis_token is not None and isinstance(redis_token, str) and redis_token != "":
                            switchFrameWithMenuName("lobby-menu")
                        else:
                            print("on_session_login_click: no valid session")
                            switchFrameWithMenuName("login-menu")
                    else:
                        print("Invalid or missing redis_token in response data.")
                else:
                    switchFrameWithMenuName("login-menu")
            except Exception as e:
                print(f"An error occurred: {e}")

        start_button.bind("<Button-1>", on_session_login_click)

        start_button.place(relx=0.397, rely=0.842, anchor="center")

        def on_program_exit_click(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('menu_button_click')
            try:
                responseData = self.__mainMenuFrameRepository.requestProgramExit(
                    ProgramExitRequest())

                print(f"responseData: {responseData}")

                if responseData and responseData.get("does_client_exit_success") is True:
                    MusicPlayerRepositoryImpl.getInstance().stopBackgroundMusic()
                    rootWindow.destroy()
                else:
                    print("응답이 잘못 되었음")
            except Exception as e:
                print(f"An error occurred: {e}")

        exit_button = tkinter.Button(mainMenuFrame,
                                     image=self.button_exit,
                                     bd=0, highlightthickness=0,
                                     width=264, height=67)
        exit_button.bind("<Button-1>", on_program_exit_click)
        exit_button.place(relx=0.605, rely=0.842, anchor="center")

        def play_mouse_on_button_sound(event):
            self.__musicPlayerRepository.play_sound_effect_of_mouse_on_click('mouse_on_button')

        start_button.bind('<Enter>', play_mouse_on_button_sound)
        exit_button.bind('<Enter>', play_mouse_on_button_sound)

        return mainMenuFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("MainMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__mainMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("MainMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__mainMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)


