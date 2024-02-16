import os
import unittest

import pandas


class TestUglyCsvRead(unittest.TestCase):

    def test_ugly_csv_read(self):
        currentLocation = os.getcwd()
        print(f"currentLocation: {currentLocation}")

        everycard = pandas.read_csv('../../../local_storage/card_info/every_card.csv')
        print(everycard)

        everycard_names = everycard['카드명']
        print(everycard_names)

        everycard_number = everycard['카드번호']
        print(everycard_number)

        everycard_column_names = everycard.columns
        print(everycard_column_names)

        selected_row = everycard[everycard['카드번호'] == 6]
        print(selected_row)




if __name__ == '__main__':
    unittest.main()

