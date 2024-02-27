import tkinter


from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl
from rock_paper_scissors.service.rock_paper_scissors_service import RockPaperScissorsService
from session.service.session_service_impl import SessionServiceImpl


class RockPaperScissorsServiceImpl(RockPaperScissorsService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__rockPaperScissorsRepositoryImpl = RockPaperScissorsRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def createRockPaperScissorsUiFrame(self, rootWindow, switchFrameWithMenuName):
        rockPaperScissorsFrame = self.__rockPaperScissorsRepositoryImpl.createRockPaperScissorsFrame(rootWindow)

        def final_decision_button_click(target_rps):
            self.__rockPaperScissorsRepositoryImpl.setRace(target_rps)




        label_text = self.__rockPaperScissorsRepositoryImpl.getRPS()
        label = tkinter.Label(rockPaperScissorsFrame, text=label_text, font=("Helvetica", 32), fg="black",
                              anchor="center", justify="center")

        label.place(relx=0.5, rely=0.8, anchor="center", bordermode="outside")  # 가운데 정렬



        self.final_decision_button = tkinter.Button(rockPaperScissorsFrame, text="선택 완료", bg="#2E2BE2", fg="white",
                                             command=lambda: final_decision_button_click(self.__rockPaperScissorsRepositoryImpl.getRPS()),
                                             width=24, height=2)
        self.final_decision_button.place(relx=0.5, rely=0.9, anchor="center")


        return rockPaperScissorsFrame



    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("CardShopMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__rockPaperScissorsRepositoryImpl.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("CardShopMenuFrameServiceImpl: injectReceiveIpcChannel()")
        self.__rockPaperScissorsRepositoryImpl.saveReceiveIpcChannel(receiveIpcChannel)