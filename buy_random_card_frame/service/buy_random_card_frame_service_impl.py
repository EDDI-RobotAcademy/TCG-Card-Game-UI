import tkinter

from card_back_frame.service.card_back_frame_service_impl import CardBackFrameServiceImpl
from buy_random_card_frame.repository.buy_random_card_frame_repository_impl import BuyRandomCardFrameRepositoryImpl
from buy_random_card_frame.service.buy_random_card_frame_service import BuyRandomCardFrameService
from buy_random_card_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from session.service.session_service_impl import SessionServiceImpl


class BuyRandomCardFrameServiceImpl(BuyRandomCardFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__buyRandomCardFrameRepository = BuyRandomCardFrameRepositoryImpl.getInstance()
            cls.__instance.__cardBackFrameService = CardBackFrameServiceImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def Gacha(self):
        testRace = self.__cardShopMenuFrameRepository.getRace()
        print(f"testRace: {testRace}")
        self.__label.configure(text=testRace)
        return testRace

    def buyRandomCardRequest(self):
        try:
            session_info = self.__sessionService.getSessionInfo()
            if session_info is not None:
                responseData = self.__buyRandomCardFrameRepository.requestBuyRandomCard(
                    BuyRandomCardRequest(sessionInfo=session_info, race=self.Gacha()))

                print(f"responseData: {responseData}")
                return responseData

            else:
                print("Invalid or missing response data.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def createBuyRandomCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        BuyRandomCardFrame = self.__buyRandomCardFrameRepository.createBuyRandomCardFrame(rootWindow)

        # responseData = self.buyRandomCardRequest()
        # print(responseData)
        # card = [value for value in responseData]



        self.__label = tkinter.Label(BuyRandomCardFrame, font=("Helvetica", 64), fg="black",
                              anchor="center", justify="center")
        self.__label.place(relx=0.3, rely=0.95, anchor="center", bordermode="outside")  # 가운데 정렬

        BuyRandomCardFrame1 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame1.place(relx=0.15, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame2 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame2.place(relx=0.33, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame3 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame3.place(relx=0.51, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame4 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame4.place(relx=0.69, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame5 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame5.place(relx=0.87, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame6 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame6.place(relx=0.15, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame7 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame7.place(relx=0.33, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame8 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame8.place(relx=0.51, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame9 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame9.place(relx=0.69, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        BuyRandomCardFrame10 = self.__cardBackFrameService.createCardBackUiFrame(BuyRandomCardFrame)
        BuyRandomCardFrame10.place(relx=0.87, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        back_to_shop_button = tkinter.Button(BuyRandomCardFrame, text="뒤로 가기", bg="#2E2BE2", fg="white",
                                              command=lambda: switchFrameWithMenuName("card-shop-menu"), width=5,
                                              height=2)
        back_to_shop_button.place(relx=0.95, rely=0.95, anchor="center")

        one_more_time_button = tkinter.Button(BuyRandomCardFrame, text="한번 더 뽑기", bg="#2E2BE2", fg="white",
                                             command=lambda: switchFrameWithMenuName("buy-random-card"), width=5,
                                             height=2)
        one_more_time_button.place(relx=0.89, rely=0.95, anchor="center")


        return BuyRandomCardFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("BuyRandomCardFrameService: injectTransmitIpcChannel()")
        self.__buyRandomCardFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("BuyRandomCardFrameService: injectTransmitIpcChannel()")
        self.__buyRandomCardFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)
