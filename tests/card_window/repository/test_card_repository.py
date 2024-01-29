import unittest

import pandas as pd

from card_info_from_csv.entity.card_rendering_entity import CardInfoFromCsv


class TestCardInfoRepositoryImpl(unittest.TestCase):


    def testRegisterCardInfo(self):
        repository = CardInfoFromCsv.getInstance()
        dataFile = pd.read_csv('../../../local_storage/card/data.csv', skiprows=1)
        dataFile.fillna(0, inplace=True)
        print(f"{dataFile.head()}")
        repository.build_dictionaries(dataFile.itertuples())
        repository.get_card_name('55')

if __name__ == '__main__':
    unittest.main()