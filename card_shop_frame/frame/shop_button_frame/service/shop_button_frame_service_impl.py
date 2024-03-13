import tkinter

from card_shop_frame.frame.shop_button_frame.service.shop_button_frame_service import ShopButtonFrameService
from card_shop_frame.frame.shop_button_frame.repository.shop_button_frame_repository_impl import ShopButtonFrameRepositoryImpl
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl

class ShopButtonFrameServiceImpl(ShopButtonFrameService):
    __instance = None
    def __new__(cls):
        from card_shop_frame.service.card_shop_service_impl import CardShopMenuFrameServiceImpl
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__shopButtonFrameRepository = ShopButtonFrameRepositoryImpl.getInstance()
            cls.__instance.__cardShopMenuFrameService = CardShopMenuFrameServiceImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.legend_stack_count = 10


    def findRace(self):
        race_mapping = {
            "전체": "Chaos",
            "언데드": "Undead",
            "트랜트": "Trent",
            "휴먼": "Human"
        }
        Race = self.__cardShopMenuFrameRepository.getRace()
        Eg_Race = race_mapping.get(Race, "Unknown")
        print(f"Eg_Race: {Eg_Race}")
        return Eg_Race


    def createShopButtonUiFrame(self, rootWindow, switchFrameWithMenuName):
        shopButtonFrame = self.__shopButtonFrameRepository.createShopButtonFrame(rootWindow)

        def chaos_button_click():
            print("chaos_button_click")

        def undead_button_click():
            print("undead_button_click")

        def trent_button_click():
            print("trent_button_click")

        def human_button_click():
            print("human_button_click")

        chaos_button = tkinter.Button(shopButtonFrame, text="chaos", command=chaos_button_click)
        undead_button = tkinter.Button(shopButtonFrame, text="Undead", command=undead_button_click)
        trent_button = tkinter.Button(shopButtonFrame, text="Trent", command=trent_button_click)
        human_button = tkinter.Button(shopButtonFrame, text="human", command=human_button_click)

        chaos_button.place(relx=0, rely=0.0, relwidth=1, relheight=0.1)
        undead_button.place(relx=0, rely=0.2, relwidth=1, relheight=0.1)
        trent_button.place(relx=0, rely=0.3, relwidth=1, relheight=0.1)
        human_button.place(relx=0, rely=0.4, relwidth=1, relheight=0.1)



        return shopButtonFrame

