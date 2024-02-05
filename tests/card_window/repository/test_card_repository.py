import unittest

from card_info_from_csv.controller.card_info_from_csv_controller_impl import CardInfoFromCsvControllerImpl
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from card_info_from_csv.service.card_info_from_csv_service_impl import CardInfoFromCsvServiceImpl


class TestCardInfoRepositoryImpl(unittest.TestCase):


    def testRegisterCardInfo(self):
        repo = CardInfoFromCsvRepositoryImpl().getInstance()
        CardInfoFromCsvServiceImpl().getInstance()
        con = CardInfoFromCsvControllerImpl().getInstance()

        con.requestToCardInfoSettingInMemory()
        print(f"{repo.getCardNameForCardNumber(8)}")

if __name__ == '__main__':
    unittest.main()