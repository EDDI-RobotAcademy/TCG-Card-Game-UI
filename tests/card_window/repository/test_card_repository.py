import unittest
from card.card_rendering.repository.card_rendering_repository_impl import CardRenderingRepositoryImpl


class TestCardInfoRepositoryImpl(unittest.TestCase):


    def testRegisterCardInfo(self):
        repository = CardRenderingRepositoryImpl()
        repository.getInstance()
        cardInfo = repository.registerCardInfo(52)
        print(cardInfo.getCardName())
        print(cardInfo.getCardRace())
        print(cardInfo.getCardType())
        print(cardInfo.getCardHealth())
        print(cardInfo.getCardAtaack())
        print(cardInfo.getCardEnergy())


if __name__ == '__main__':
    unittest.main()