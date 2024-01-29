import unittest

import pandas as pd

from card_info_from_csv.entity.card_rendering_entity import CardInfoFromCsv


class TestCardInfoRepositoryImpl(unittest.TestCase):


    def testRegisterCardInfo(self):
        repository = CardInfoFromCsv.getInstance()
        dataFile = repository.read_card_data('../../../local_storage/card/data.csv')
        repository.build_dictionaries(dataFile)
        card_name = repository.get_card_name(8)
        print(card_name)

if __name__ == '__main__':
    unittest.main()