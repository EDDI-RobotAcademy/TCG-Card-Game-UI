import tkinter
from PIL import ImageTk, Image

from rock_paper_scissors.repository.rock_paper_scissors_repository_impl import RockPaperScissorsRepositoryImpl
from rock_paper_scissors.service.rock_paper_scissors_service import RockPaperScissorsService
from rock_paper_scissors.service.request.rock_paper_scissors_request import RockPaperScissorsRequest
from session.repository.session_repository_impl import SessionRepositoryImpl
from rock_paper_scissors.frame.check_rock_paper_scissors_winner.service.check_rock_paper_scissors_winner_service_impl import CheckRockPaperScissorsWinnerServiceImpl


class RockPaperScissorsServiceImpl(RockPaperScissorsService):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__rockPaperScissorsRepositoryImpl = RockPaperScissorsRepositoryImpl.getInstance()
            cls.__instance.__sessionRepositoryImpl = SessionRepositoryImpl.getInstance()
            cls.__instance.__checkRockPaperScissorsWinnerServiceImpl = CheckRockPaperScissorsWinnerServiceImpl()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def findRPS(self):
        RPS_mapping = {
            "보": "Paper",
            "가위": "Scissors",
            "바위": "Rock"
        }
        RPS = self.__rockPaperScissorsRepositoryImpl.getRPS()
        Eg_RPS = RPS_mapping.get(RPS, "Unknown")
        return Eg_RPS

    def createRockPaperScissorsUiFrame(self, rootWindow, switchFrameWithMenuName):
        rockPaperScissorsFrame = self.__rockPaperScissorsRepositoryImpl.createRockPaperScissorsFrame(rootWindow)

        def final_decision_button_click(target_rps):
            print(f"target_rps: {target_rps}")
            responseData = self.__rockPaperScissorsRepositoryImpl.requestRockPaperScissors(
                RockPaperScissorsRequest(self.__sessionRepositoryImpl.get_session_info(), target_rps))
            print(f"responseData: {responseData}")
            if responseData.get("is_success") is True:
                self.__checkRockPaperScissorsWinnerServiceImpl.createCheckRockPaperScissorsWinnerUiFrame(
                    rockPaperScissorsFrame, switchFrameWithMenuName)


        def on_paper_image_click(event):
            self.__rockPaperScissorsRepositoryImpl.setRPS("보")
            RPS_label.config(text=self.__rockPaperScissorsRepositoryImpl.getRPS())

        image_path = "/home/eddi/proj/TCG-Card-Game-UI/local_storage/rock_paper_scissors_image/paper.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 250), Image.LANCZOS)
        self.__paper_image = ImageTk.PhotoImage(resized_image)

        paper_label = tkinter.Label(rockPaperScissorsFrame, image=self.__paper_image)
        paper_label.place(x=450, y=200)
        paper_label.bind("<Button-1>", on_paper_image_click)

        def on_scissors_image_click(event):
            self.__rockPaperScissorsRepositoryImpl.setRPS("가위")
            RPS_label.config(text=self.__rockPaperScissorsRepositoryImpl.getRPS())

        image_path = "/home/eddi/proj/TCG-Card-Game-UI/local_storage/rock_paper_scissors_image/scissors.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 250), Image.LANCZOS)
        self.__scissors_image = ImageTk.PhotoImage(resized_image)

        scissors_label = tkinter.Label(rockPaperScissorsFrame, image=self.__scissors_image)
        scissors_label.place(x=750, y=200)
        scissors_label.bind("<Button-1>", on_scissors_image_click)

        def on_rock_image_click(event):
            self.__rockPaperScissorsRepositoryImpl.setRPS("바위")
            RPS_label.config(text=self.__rockPaperScissorsRepositoryImpl.getRPS())

        image_path = "/home/eddi/proj/TCG-Card-Game-UI/local_storage/rock_paper_scissors_image/rock.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 250), Image.LANCZOS)
        self.__rock_image = ImageTk.PhotoImage(resized_image)

        rock_label = tkinter.Label(rockPaperScissorsFrame, image=self.__rock_image)
        rock_label.place(x=1050, y=200)
        rock_label.bind("<Button-1>", on_rock_image_click)


        label_text = self.__rockPaperScissorsRepositoryImpl.getRPS()
        RPS_label = tkinter.Label(rockPaperScissorsFrame, text=label_text, font=("Helvetica", 32), fg="black",
                              anchor="center", justify="center")

        RPS_label.place(relx=0.5, rely=0.8, anchor="center", bordermode="outside")  # 가운데 정렬



        self.final_decision_button = tkinter.Button(rockPaperScissorsFrame, text="선택 완료", bg="#2E2BE2", fg="white",
                                             command=lambda: final_decision_button_click(self.findRPS()),
                                             width=24, height=2)
        self.final_decision_button.place(relx=0.5, rely=0.9, anchor="center")


        return rockPaperScissorsFrame



    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("CardShopMenuFrameServiceImpl: injectTransmitIpcChannel()")
        self.__rockPaperScissorsRepositoryImpl.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("CardShopMenuFrameServiceImpl: injectReceiveIpcChannel()")
        self.__rockPaperScissorsRepositoryImpl.saveReceiveIpcChannel(receiveIpcChannel)