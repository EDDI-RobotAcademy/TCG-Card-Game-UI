from tkinter import ttk
import tkinter as tk



from opengl_buy_random_card_frame.entity.buy_random_card_scene import BuyRandomCardScene
from opengl_buy_random_card_frame.frame.buy_random_card_frame import BuyRandomCardFrame
from opengl_buy_random_card_frame.service.buy_random_card_frame_service import BuyRandomCardFrameService
from opengl_buy_random_card_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from opengl_button.button_binding.buy_random_card_button_bind import BuyRandomCardFrameButtonBind

from session.service.session_service_impl import SessionServiceImpl
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
            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def Gacha(self):
        testRace = self.__cardShopMenuFrameRepository.getRace()
        print(f"testRace: {testRace}")
        return testRace


    def requestBuyRandomCard(self, buyRandomCardRequest):
        print(f"BuyRandomCardFrameRepositoryImpl: requestBuyRandomCard() -> {buyRandomCardRequest}")

        self.__transmitIpcChannel.put(buyRandomCardRequest)
        return self.__receiveIpcChannel.get()

    def buyRandomCardRequest(self):
        try:
            session_info = self.__sessionService.getSessionInfo()
            if session_info is not None:
                responseData = self.requestBuyRandomCard(
                    BuyRandomCardRequest(sessionInfo=session_info, race=self.Gacha()))

                print(f"responseData: {responseData}")
                return responseData

            else:
                print("Invalid or missing response data.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def createBuyRandomCardUiFrame(self, rootWindow, switchFrameWithMenuName):
        # responseData = self.buyRandomCardRequest()
        # print(responseData)
        # self.__buyRandomCardScene.add_card_list(responseData)

        buyRandomCardrame = self.__buyRandomCardFrame(rootWindow)

        buttonBinding = BuyRandomCardFrameButtonBind(master=rootWindow, frame=buyRandomCardrame)
        buttonBinding.button_bind()




        return buyRandomCardrame
