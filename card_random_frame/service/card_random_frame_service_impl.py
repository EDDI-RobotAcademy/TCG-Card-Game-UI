import tkinter

from card_back_frame.service.card_back_frame_service_impl import CardBackFrameServiceImpl
from card_random_frame.repository.card_random_frame_repository_impl import CardRandomFrameRepositoryImpl
from card_random_frame.service.card_random_frame_service import CardRandomFrameService


class CardRandomFrameServiceImpl(CardRandomFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardRandomFrameRepository = CardRandomFrameRepositoryImpl.getInstance()
            cls.__instance.__cardBackFrameService = CardBackFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardRandomUiFrame(self, rootWindow, switchFrameWithMenuName):
        CardRandomFrame = self.__cardRandomFrameRepository.createCardRandomFrame(rootWindow)

        CardRandomFrame1 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame1.place(relx=0.15, rely=0.25, relwidth=0.15, relheight=0.38,anchor="center")

        CardRandomFrame2 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame2.place(relx=0.33, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame3 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame3.place(relx=0.51, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame4 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame4.place(relx=0.69, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame5 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame5.place(relx=0.87, rely=0.25, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame6 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame6.place(relx=0.15, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame7 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame7.place(relx=0.33, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame8 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame8.place(relx=0.51, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame9 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame9.place(relx=0.69, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        CardRandomFrame10 = self.__cardBackFrameService.createCardBackUiFrame(CardRandomFrame)
        CardRandomFrame10.place(relx=0.87, rely=0.70, relwidth=0.15, relheight=0.38, anchor="center")

        back_to_shop_button = tkinter.Button(CardRandomFrame, text="뒤로 가기", bg="#2E2BE2", fg="white",
                                              command=lambda: switchFrameWithMenuName("card-shop-menu"), width=5,
                                              height=2)
        back_to_shop_button.place(relx=0.95, rely=0.95, anchor="center")

        one_more_time_button = tkinter.Button(CardRandomFrame, text="한번 더 뽑기", bg="#2E2BE2", fg="white",
                                             command=lambda: switchFrameWithMenuName("card-shop-menu"), width=5,
                                             height=2)
        one_more_time_button.place(relx=0.89, rely=0.95, anchor="center")


        return CardRandomFrame