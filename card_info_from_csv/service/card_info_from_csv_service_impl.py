import os

from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from card_info_from_csv.service.card_info_from_csv_service import CardInfoFromCsvService

from common.utility import get_project_root


class CardInfoFromCsvServiceImpl(CardInfoFromCsvService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__cardInfoFromCsvRepositoryImpl = CardInfoFromCsvRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance


    def cardInfoSettingInMemory(self):
        project_root = get_project_root()

        dataFile = self.__cardInfoFromCsvRepositoryImpl.readCardData(os.path.join(project_root, 'local_storage', 'card', 'data.csv'))
        self.__cardInfoFromCsvRepositoryImpl.build_dictionaries(dataFile)
        print("Setting On")