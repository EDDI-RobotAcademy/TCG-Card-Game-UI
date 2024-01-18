from card.card_rendering.controller.card_rendering_controller import CardRenderingController


class CardRenderingControllerImpl(CardRenderingController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def cardRender(self, cardNumber, cardSize):
        pass