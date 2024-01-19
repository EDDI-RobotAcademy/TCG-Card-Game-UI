import unittest
from card.card_rendering.repository.card_rendering_repository_impl import CardRenderingRepositoryImpl


class TestCardInfoRepositoryImpl(unittest.TestCase):


    def testRegisterCardInfo(self):
        repository = CardRenderingRepositoryImpl()
        repository.getInstance()
        cardInfo = repository.registerCardInfo(6)
        print(cardInfo)


if __name__ == '__main__':
    unittest.main()