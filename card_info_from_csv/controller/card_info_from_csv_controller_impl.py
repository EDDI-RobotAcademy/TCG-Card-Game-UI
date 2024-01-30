from card_info_from_csv.controller.card_info_from_csv_controller import CardInfoFromCsvController
from card_info_from_csv.service.card_info_from_csv_service_impl import CardInfoFromCsvServiceImpl


class CardInfoFromCsvControllerImpl(CardInfoFromCsvController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardInfoFromCsvServiceImpl = CardInfoFromCsvServiceImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestToCardInfoSettingInMemory(self):
        self.__cardInfoFromCsvServiceImpl.cardInfoSettingInMemory()
