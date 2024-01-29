from card_info_from_csv.repository.card_rendering_repository_impl import CardRenderingRepositoryImpl
from card_info_from_csv.service.card_rendering_service import CardRenderingService


class CardRenderingServiceImpl(CardRenderingService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardRenderingRepository = CardRenderingRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def registerCardRenderingInfo(self, cardNumber):
        return self.__cardRenderingRepository.registerCardInfo(cardNumber)
