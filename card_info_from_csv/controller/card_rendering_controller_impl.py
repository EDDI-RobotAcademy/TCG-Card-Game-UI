from card_info_from_csv.controller.card_rendering_controller import CardRenderingController
from card_info_from_csv.service.card_rendering_service_impl import CardRenderingServiceImpl


class CardRenderingControllerImpl(CardRenderingController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardRenderingService = CardRenderingServiceImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestToCardRenderingCardNumber(self, cardNumber):
        card_info = self.__cardRenderingService.registerCardRenderingInfo(cardNumber)
