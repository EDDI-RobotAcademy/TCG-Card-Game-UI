from tkinter import Label

from card_shop_frame.frame.my_game_money_frame.repository.my_game_money_frame_repository_impl import MyGameMoneyFrameRepositoryImpl
from card_shop_frame.frame.my_game_money_frame.service.my_game_money_frame_service import MyGameMoneyFrameService
from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl


class MyGameMoneyFrameServiceImpl(MyGameMoneyFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myGameMoneyFrameRepository = MyGameMoneyFrameRepositoryImpl.getInstance()
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
            cls.__instance.__money_image = None
            cls.__instance.__label_GameMoney = None

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def findMyMoney(self):
        myMoney = self.__cardShopMenuFrameRepository.getMyMoney()
        print(f"myMoney: {myMoney}")
        self.__label_GameMoney.configure(text=myMoney)


    def createMyGameMoneyUiFrame(self, rootWindow):
        myGameMoneyFrame = self.__myGameMoneyFrameRepository.createMyGameMoneyFrame(rootWindow)

        # image_path = '/home/eddi/proj/TCG-Card-Game-UI/images/game_money.png'
        # original_image = Image.open(image_path)
        # resized_image = original_image.resize((15, 15), Image.LANCZOS)
        # self.__money_image = ImageTk.PhotoImage(resized_image)

        self.__label_GameMoney = Label(myGameMoneyFrame, image=self.__money_image, compound="left",
                                       font=("Arial", 12))
        self.__label_GameMoney.pack()


        return myGameMoneyFrame
