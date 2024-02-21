from opengl_buy_random_card_frame.entity.buy_random_card_scene import BuyRandomCardScene
from opengl_buy_random_card_frame.frame.buy_random_card_frame import BuyRandomCardFrame
from opengl_buy_random_card_frame.service.buy_random_card_frame_service import BuyRandomCardFrameService
from card_shop_frame.frame.buy_check_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from opengl_button.button_binding.buy_random_card_button_bind import BuyRandomCardFrameButtonBind

from session.repository.session_repository_impl import SessionRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl


class BuyRandomCardFrameServiceImpl(BuyRandomCardFrameService):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__buyRandomCardFrame = BuyRandomCardFrame
            cls.__instance.__buyRandomCardScene = BuyRandomCardScene()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBuyRandomCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        # responseData = self.buyRandomCardRequest()
        # print(responseData)
        # self.__buyRandomCardScene.add_card_list(responseData)

        buyRandomCardrame = self.__buyRandomCardFrame(rootWindow)

        buttonBinding = BuyRandomCardFrameButtonBind(master=rootWindow, frame=buyRandomCardrame)
        buttonBinding.button_bind()

        return buyRandomCardrame
