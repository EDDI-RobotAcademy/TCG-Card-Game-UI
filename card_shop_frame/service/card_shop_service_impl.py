import tkinter

from card_shop_frame.repository.card_shop_repository_impl import CardShopMenuFrameRepositoryImpl
from card_shop_frame.service.card_shop_service import CardShopMenuFrameService


class CardShopMenuFrameServiceImpl(CardShopMenuFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardShopMenuFrameRepository = CardShopMenuFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createCardShopUiFrame(self, rootWindow, switchFrameWithMenuName):
        cardShopMenuFrame = self.__cardShopMenuFrameRepository.createCardShopMenuFrame(rootWindow)

        label_text = "상점"
        label = tkinter.Label(cardShopMenuFrame, text=label_text, font=("Helvetica", 64), fg="black",
                              anchor="center", justify="center")

        label.place(relx=0.5, rely=0.1, anchor="center", bordermode="outside")  # 가운데 정렬

        get_new_cards_button = tkinter.Button(cardShopMenuFrame, text="카드 뽑기", bg="#2E2BE2", fg="white",
                                                command=lambda: switchFrameWithMenuName("buy-random-card"), width=36,
                                                height=4)
        get_new_cards_button.place(relx=0.5, rely=0.5, anchor="center")

        go_back_to_lobby_button = tkinter.Button(cardShopMenuFrame, text="로비로 돌아가기", bg="#2E2BE2", fg="white",
                                        command=lambda: switchFrameWithMenuName("lobby-menu"), width=24,
                                        height=2)
        go_back_to_lobby_button.place(relx=0.2, rely=0.9, anchor="center")

        my_card_button = tkinter.Button(cardShopMenuFrame, text="내 카드 바로가기", bg="#2E2BE2", fg="white",
                                                 command=lambda: switchFrameWithMenuName("my-card-main"), width=24,
                                                 height=2)
        my_card_button.place(relx=0.8, rely=0.9, anchor="center")

        return cardShopMenuFrame
