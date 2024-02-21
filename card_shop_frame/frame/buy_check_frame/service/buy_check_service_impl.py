import tkinter

from card_shop_frame.frame.buy_check_frame.service.buy_check_service import BuyCheckService
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository_impl import BuyCheckRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from card_shop_frame.frame.buy_check_frame.service.request.free_random_card_request import FreeRandomCardRequest
from card_shop_frame.frame.buy_check_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class BuyCheckServiceImpl(BuyCheckService):
    __instance = None
    def __new__(cls):
        from card_shop_frame.service.card_shop_service_impl import CardShopMenuFrameServiceImpl
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__buyCheckRepository = BuyCheckRepositoryImpl.getInstance()
            cls.__instance.__cardShopMenuFrameService = CardShopMenuFrameServiceImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def findRace(self):
        Race = self.__cardShopMenuFrameRepository.getRace()
        print(f"Race: {Race}")
        return Race


    def createBuyCheckUiFrame(self, rootWindow, switchFrameWithMenuName):
        buyCheckFrame = self.__buyCheckRepository.createBuyCheckFrame(rootWindow)

        def restore_frame(buyCheckFrame):
            self.__cardShopMenuFrameService.RestoreCardShopUiButton()
            buyCheckFrame.destroy()

        def yes_click_button(buyCheckFrame):

            responseData = self.__buyCheckRepository.requestBuyRandomCard(
                BuyRandomCardRequest(sessionInfo=self.__sessionRepository.get_session_info(), race=self.findRace())),
            if responseData is True:
                self.__cardShopMenuFrameService.RestoreCardShopUiButton()
                switchFrameWithMenuName("buy-random-card")
                buyCheckFrame.destroy()
            else:
                self.__cardShopMenuFrameService.RestoreCardShopUiButton()
                buyCheckFrame.destroy()

        check_label = tkinter.Label(buyCheckFrame, text="100골드를 사용하여\n"+self.findRace()+" 카드 뽑기를 구매하시겠습니까?",
                                    font=("Helvetica", 28), fg="black",
                                    anchor="center", justify="center")
        check_label.place(relx=0.5, rely=0.3, anchor="center", bordermode="outside")

        yes_button = tkinter.Button(buyCheckFrame, text="예", bg="#2E2BE2", fg="white",
                                              command=lambda: yes_click_button(buyCheckFrame), width=24,
                                              height=2)

        yes_button.place(relx=0.25, rely=0.9, anchor="center")

        no_button = tkinter.Button(buyCheckFrame, text="아니오", bg="#2E2BE2", fg="white",
                                    command=lambda: restore_frame(buyCheckFrame), width=24,
                                    height=2)

        no_button.place(relx=0.75, rely=0.9, anchor="center")

        buyCheckFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        return buyCheckFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("BuyCheckServiceImpl: injectTransmitIpcChannel()")
        self.__buyCheckRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("BuyCheckServiceImpl: injectReceiveIpcChannel()")
        self.__buyCheckRepository.saveReceiveIpcChannel(receiveIpcChannel)
