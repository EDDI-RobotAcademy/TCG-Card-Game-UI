from tkinter import ttk
import tkinter as tk


from opengl_buy_random_card_frame.entity.buy_random_card_scene import BuyRandomCardScene
from opengl_buy_random_card_frame.frame.buy_random_card_frame import BuyRandomCardFrame
from opengl_buy_random_card_frame.service.buy_random_card_frame_service import BuyRandomCardFrameService
from opengl_buy_random_card_frame.service.request.buy_random_card_request import BuyRandomCardRequest
from session.service.session_service_impl import SessionServiceImpl


class BuyRandomCardFrameServiceImpl(BuyRandomCardFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__buyRandomCardFrame = BuyRandomCardFrame
            cls.__instance.__buyRandomCardScene = BuyRandomCardScene()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

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
        # responseData = self.buyRandomCardRequest()
        # print(responseData)
        # self.__buyRandomCardScene.add_card_list(responseData)

        buyRandomCardrame = self.__buyRandomCardFrame(rootWindow)




        return buyRandomCardrame
