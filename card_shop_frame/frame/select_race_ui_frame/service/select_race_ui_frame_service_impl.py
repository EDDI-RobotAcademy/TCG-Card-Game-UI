import tkinter
from PIL import ImageTk, Image

from card_shop_frame.frame.select_race_ui_frame.service.select_race_ui_frame_service import SelectRaceUiFrameService
from card_shop_frame.frame.select_race_ui_frame.repository.select_race_ui_frame_repository_impl import SelectRaceUiFrameRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from card_shop_frame.frame.buy_check_frame.service.buy_check_service_impl import BuyCheckServiceImpl
from session.repository.session_repository_impl import SessionRepositoryImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage



class SelectRaceUiFrameServiceImpl(SelectRaceUiFrameService):
    __instance = None
    __neder_image = None
    undead_mythical_cards = [19, 45, 134, 176]
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__selectRaceUiFrameRepository = SelectRaceUiFrameRepositoryImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__buyCheckService = BuyCheckServiceImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__preDrawedImageInstance = PreDrawedImage.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance



    def createSelectRaceUiFrame(self, rootWindow, switchFrameWithMenuName):
        selectRaceUiFrame = self.__selectRaceUiFrameRepository.createSelectRaceUiFrame(rootWindow)

        def cardProbabilityInfoButtonClick():
            print("카드확률 창")

        def buy_check_button_click(race):
            self.__cardShopMenuFrameRepository.setRace(race)
            self.__buyCheckService.createBuyCheckUiFrame(rootWindow, switchFrameWithMenuName)

        def undead_mythical_cards():
            for number in self.undead_mythical_cards:
                resized_undead_image = self.__preDrawedImageInstance.get_pre_draw_shop_mythical_card_illustration(19)
                if resized_undead_image is not None:
                    self.__neder_image = ImageTk.PhotoImage(resized_undead_image)
                    neder_label.config(image=self.__neder_image)
            #selectRaceUiFrame.


        neder_label = tkinter.Label(selectRaceUiFrame, image=self.__neder_image)
        neder_label.place(relx=0.1, rely=0.1, anchor=tkinter.NW)


        card_probability_info_button = tkinter.Button(selectRaceUiFrame, command=cardProbabilityInfoButtonClick, text="확률 정보")
        card_probability_info_button.place(relx=0.8, rely=0.6, relwidth=0.1, relheight=0.1)

        buy_select_race_card_button = tkinter.Button(selectRaceUiFrame, text="1 팩 구매", command=lambda:buy_check_button_click("언데드"))
        buy_select_race_card_button.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

        return selectRaceUiFrame

