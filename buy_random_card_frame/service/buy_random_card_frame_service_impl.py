import tkinter

from card_back_frame.service.card_back_frame_service_impl import CardBackFrameServiceImpl
from buy_random_card_frame.repository.buy_random_card_frame_repository_impl import BuyRandomCardFrameRepositoryImpl
from buy_random_card_frame.service.buy_random_card_frame_service import BuyRandomCardFrameService
from buy_random_card_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl


class BuyRandomCardFrameServiceImpl(BuyRandomCardFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__buyRandomCardFrameRepository = BuyRandomCardFrameRepositoryImpl.getInstance()
            cls.__instance.__cardBackFrameService = CardBackFrameServiceImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBuyRandomCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        BuyRandomCardFrame = self.__buyRandomCardFrameRepository.createBuyRandomCardFrame(rootWindow)

        # responseData = self.__buyRandomCardFrameRepository.requestBuyRandomCard(
        #         BuyRandomCardRequest())
        # print(responseData)

        testRace = self.__cardShopMenuFrameRepository.getRace()
        label = tkinter.Label(BuyRandomCardFrame, text=testRace, font=("Helvetica", 64), fg="black",
                              anchor="center", justify="center")
        label.place(relx=0.3, rely=0.95, anchor="center", bordermode="outside")  # 가운데 정렬

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
