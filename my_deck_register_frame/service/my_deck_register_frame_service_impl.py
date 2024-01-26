from tkinter import ttk

from my_deck_register_frame.frame.my_deck_register_frame import MyDeckRegisterFrame
from my_deck_register_frame.repository.my_deck_register_frame_repository_impl import MyDeckRegisterFrameRepositoryImpl
from my_deck_register_frame.service.my_deck_register_frame_service import MyDeckRegisterFrameService
from my_deck_register_frame.service.request.my_deck_register_request import MyDeckRegisterRequest
from session.service.session_service_impl import SessionServiceImpl


class MyDeckRegisterFrameServiceImpl(MyDeckRegisterFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myDeckRegisterFrameRepository = MyDeckRegisterFrameRepositoryImpl.getInstance()
            cls.__instance.__myDeckRegisterFrame = MyDeckRegisterFrame
            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyDeckRegisterUiFrame(self, rootWindow, switchFrameWithMenuName):
        myDeckRegisterFrame = self.__myDeckRegisterFrame(rootWindow)

        style = ttk.Style()
        style.configure("TFrame", background="#444444")
        style.configure("TLabel", background="#444444", foreground="#ffffff", font=("Arial", 12))
        style.configure("TButton", background="#2C3E50", foreground="#ffffff", font=("Arial", 12), padding=(10, 5))

        label_deckname = ttk.Label(myDeckRegisterFrame, text="덱 이름:", style="TLabel")
        entry_deckname = ttk.Entry(myDeckRegisterFrame, font=("Arial", 12))

        button_register_deck = ttk.Button(myDeckRegisterFrame, text="확인", style="TButton")

        def on_deck_register_click(event):
            try:
                session_info = self.__sessionService.getSessionInfo()
                if session_info is not None:
                    responseData = self.__myDeckRegisterFrameRepository.requestRegister(
                        MyDeckRegisterRequest(session_info, entry_deckname.get()))

                    print(f"responseData: {responseData}")

                    if responseData and responseData.get("is_success") is True:
                        switchFrameWithMenuName("my_card-main")
                    else:
                        print("Invalid or missing response data.")

            except Exception as e:
                print(f"An error occurred: {e}")

        button_register_deck.bind("<Button-1>", on_deck_register_click)

        label_deckname.place(relx=0.44, rely=0.4, anchor="center")
        entry_deckname.place(relx=0.56, rely=0.4, anchor="center")

        myDeckRegisterFrame.init_shapes()

        button_register_deck.place(relx=0.5, rely=0.6, anchor="center")

        return myDeckRegisterFrame


    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__myDeckRegisterFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__myDeckRegisterFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)