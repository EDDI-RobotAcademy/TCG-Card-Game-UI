import tkinter

from main_frame.repository.main_menu_frame_repository_impl import MainMenuFrameRepositoryImpl
from main_frame.service.main_menu_frame_service import MainMenuFrameService
from main_frame.service.request.program_exit_request import ProgramExitRequest
from session.service.session_service_impl import SessionServiceImpl


class MainMenuFrameServiceImpl(MainMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__mainMenuFrameRepository = MainMenuFrameRepositoryImpl.getInstance()

            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMainUiFrame(self, rootWindow, switchFrameWithMenuName):
        mainMenuFrame = self.__mainMenuFrameRepository.createMainMenuFrame(rootWindow)

        label_text = "EDDI TCG Card Battle"
        label = tkinter.Label(mainMenuFrame, text=label_text, font=("Helvetica", 72), bg="black", fg="white",
                              anchor="center", justify="center", pady=50)

        label.place(relx=0.5, rely=0.5, anchor="center", bordermode="outside")  # 가운데 정렬

        # start_button = tkinter.Button(mainMenuFrame, text="시작", bg="#2E7D32", fg="white",
        #                               command=lambda: switchFrameWithMenuName("login-menu"), width=36, height=2)
        start_button = tkinter.Button(mainMenuFrame, text="시작", bg="#2E7D32", fg="white", width=36, height=2)

        def on_session_login_click(event):
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

        start_button.place(relx=0.5, rely=0.65, anchor="center")

        def on_program_exit_click(event):
            try:
                responseData = self.__mainMenuFrameRepository.requestProgramExit(
                    ProgramExitRequest())

                print(f"responseData: {responseData}")

                if responseData and responseData.get("is_success") is True:
                    rootWindow.quit()
                else:
                    print("응답이 잘못 되었음")
            except Exception as e:
                print(f"An error occurred: {e}")

        exit_button = tkinter.Button(mainMenuFrame, text="종료", bg="#C62828", fg="white", width=36, height=2)
        exit_button.bind("<Button-1>", on_program_exit_click)
        exit_button.place(relx=0.5, rely=0.75, anchor="center")

        return mainMenuFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("MainMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__mainMenuFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("MainMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__mainMenuFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)


