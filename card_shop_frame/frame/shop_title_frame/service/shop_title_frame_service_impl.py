import tkinter

from card_shop_frame.frame.shop_title_frame.repository.shop_title_frame_repository_impl import ShopTitleFrameRepositoryImpl
from card_shop_frame.frame.shop_title_frame.service.shop_title_frame_service import ShopTitleFrameService
from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service_impl import MyGameMoneyFrameServiceImpl


class ShopTitleFrameServiceImpl(ShopTitleFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__shopTitleFrameRepository = ShopTitleFrameRepositoryImpl.getInstance()
            cls.__instance.__myGameMoneyFrameService = MyGameMoneyFrameServiceImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def createShopTitleUiFrame(self, rootWindow, switchFrameWithMenuName):
        shopTitleFrame = self.__shopTitleFrameRepository.createShopTitleFrame(rootWindow)

        go_to_lobby_button = tkinter.Button(shopTitleFrame, text="Lobby",
                                            command=lambda: switchFrameWithMenuName("lobby-menu"))
        go_to_lobby_button.place(relx=0.05, rely=0.4, relwidth=0.1, relheight=0.2)

        label_shop_title = tkinter.Label(shopTitleFrame, compound="left", font=("Arial", 12), text="상점")
        label_shop_title.place(relx=0.3, rely=0.4, anchor=tkinter.W)

        my_money_frame = self.__myGameMoneyFrameService.createMyGameMoneyUiFrame(shopTitleFrame)
        my_money_frame.place(relx=0.91, rely=0.4, relwidth=0.1, relheight=0.15, anchor="center")




        return shopTitleFrame
